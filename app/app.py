from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from sqlalchemy.exc import SQLAlchemyError
import os
from logging.handlers import RotatingFileHandler
import re

# Load environment variables, or use defualt 'sqlite:///users.db'
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///users.db')

# Set up logging to write logs to a rotating file
log_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Create Flask app
app = Flask("Prima")
app.logger.addHandler(log_handler)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

# Define User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        # Set the user's password using password hashing.
        self.password_hash = generate_password_hash(password)

# API Endpoint to create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        # Get JSON data from the request
        data = request.json

        # Validate input data
        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            # Log an error and return a response for invalid data
            error_message = f"Invalid data. Required fields: {', '.join(required_fields)}"
            app.logger.error(error_message)
            return jsonify({'error': error_message}), 400

        # Validate password strength
        password = data['password']
        # Check for minimum character limit
        if len(password) < 8:
            error_message = "Password must be at least 8 characters long."
            app.logger.error(error_message)
            return jsonify({'error': error_message}), 400

        # Check for at least one capital letter
        if not any(char.isupper() for char in password):
            error_message = "Password must contain at least one capital letter."
            app.logger.error(error_message)
            return jsonify({'error': error_message}), 400
        
        # Check for at least one number
        if not any(char.isdigit() for char in password):
            error_message = "Password must contain at least one number."
            app.logger.error(error_message)
            return jsonify({'error': error_message}), 400
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*()_+{}|":;<>,.?/~`]', password):
            error_message = "Password must contain at least one special character."
            app.logger.error(error_message)
            return jsonify({'error': error_message}), 400
        
        # Check if the email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            # Log an error and return a response for existing email
            error_message = 'Email already exists'
            app.logger.error(error_message)
            return jsonify({'error': error_message}), 400

        # Create a new User object and set the hashed password
        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])

        # Add the new user to the database session
        db.session.add(new_user)

        # Commit the changes to the database
        db.session.commit()

        # Return a response indicating success
        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

    except SQLAlchemyError as e:
        # Log the specific database-related exception and return a response
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        # Log other exceptions for debugging purposes and return a response
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# API Endpoint to retrieve user information by user ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Query the database for the user with the given ID
        user = User.query.get(user_id)

        # Check if the user was not found
        if user is None:
            # Log an error and return a response for user not found
            error_message = 'User not found'
            app.logger.error(error_message)
            return jsonify({'error': error_message}), 404

        # Return user information in the response
        return jsonify({'user_id': user.id, 'username': user.username, 'email': user.email})

    except SQLAlchemyError as e:
        # Log the specific database-related exception and return a response
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        # Log other exceptions for debugging purposes and return a response
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Run the Flask app
if __name__ == '__main__':
    # Create the application context before running the app
    with app.app_context():
        # Create the database tables
        db.create_all()

    # Flask development server to run with debugging, to listen on all network interfaces, and to use port 8080.
    # NOTE: This is for dev purposes, turn debug off and only listen on required server for prod env
    app.run(debug=True, host='0.0.0.0', port=8080)

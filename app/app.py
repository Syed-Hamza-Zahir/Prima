from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from sqlalchemy.exc import SQLAlchemyError
import os

# Load environment variables
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///users.db')

# Set up logging to write logs to a file
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')  # Change the level as needed

# Create Flask app
app = Flask("Prima")

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
        if 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Invalid data. Required fields: username, email, password'}), 400

        # Check if the email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400

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
        # Log the specific database-related exception
        logging.error(f"Database error occurred: {str(e)}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        # Log other exceptions for debugging purposes
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# API Endpoint to retrieve user information by user ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Query the database for the user with the given ID
        user = User.query.get(user_id)

        # Check if the user was not found
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        # Return user information in the response
        return jsonify({'user_id': user.id, 'username': user.username, 'email': user.email})

    except SQLAlchemyError as e:
        # Log the specific database-related exception
        logging.error(f"Database error occurred: {str(e)}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        # Log other exceptions for debugging purposes
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Run the Flask app
if __name__ == '__main__':
    # Create the application context before running the app
    with app.app_context():
        # Create the database tables
        db.create_all()

    # Flask development server to run with debugging disabled, to listen on all network interfaces, and to use port 8080.
    app.run(debug=False, host='0.0.0.0', port=8080)



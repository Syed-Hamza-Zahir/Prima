from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Create Flask app
app = Flask("Prima")

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
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

# API Endpoint to retrieve user information by user ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Query the database for the user with the given ID
    user = User.query.get(user_id)

    # Check if the user was not found
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Return user information in the response
    return jsonify({'user_id': user.id, 'username': user.username, 'email': user.email})

# Run the Flask app
if __name__ == '__main__':
    # Create the application context before running the app
    with app.app_context():
        # Create the database tables
        db.create_all()

    # Run the Flask app
    app.run(debug=True)

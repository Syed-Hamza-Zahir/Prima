# Import necessary modules from Flask
from flask import Flask, request, jsonify

# Create Flask app named "Prima"
app = Flask("Prima")

# Define a simple in-memory database for now
user_db = {}

# Create a simple User class for the data model
class User:
    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password

# API Endpoint to create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    # Get JSON data from the request
    data = request.json

    # Validate input data
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data. Required fields: username, email, password'}), 400

    # Generate a unique user ID 
    user_id = len(user_db) + 1

    # Create a new User object
    new_user = User(user_id, data['username'], data['email'], data['password'])

    # Store the user in the database
    user_db[user_id] = new_user.__dict__

    return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201

# API Endpoint to retrieve user information by user ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Check if the user ID exists in the database
    if user_id not in user_db:
        return jsonify({'error': 'User not found'}), 404

    # Return user information
    return jsonify(user_db[user_id])

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

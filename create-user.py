import requests
import re

# Define the API endpoint
api_url = "http://localhost:5000/api/users"

# Example user data
username = input("Enter username: ")
email = input("Enter email: ")

# Validate password input
while True: 
    password = input("Enter password: ")

    # Check for minimum character limit
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        continue

    # Check for at least one capital letter
    if not any(char.isupper() for char in password):
        print("Password must contain at least one capital letter.")
        continue

    # Check for at least one number
    if not any(char.isdigit() for char in password):
        print("Password must contain at least one number.")
        continue

    # Check for at least one special character
    if not re.search(r'[!@#$%^&*()_+{}|":;<>,.?/~`]', password):
        print("Password must contain at least one special character.")
        continue

    # All checks passed, break out of the loop
    break

# Create user data dictionary
user_data = {
    "username": username,
    "email": email,
    "password": password
}

# Make a POST request to create the user
response = requests.post(api_url, json=user_data)

# Print the response
print(response.status_code)
print(response.json())

# Check if the user was created successfully
if response.status_code == 201:
    print("User created successfully")
else:
    # Print an error message if user creation failed
    print(f"User creation failed. Status code: {response.status_code}")

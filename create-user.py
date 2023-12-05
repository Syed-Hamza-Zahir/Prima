import requests

# Define the API endpoint
api_url = "http://localhost:5000/api/users"

# Example user data
username = input("Enter username: ")
email = input("Enter email: ")
password = input("Entre password: ")

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

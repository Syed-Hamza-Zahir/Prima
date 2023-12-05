import requests

# Define the API endpoint
api_url = "http://localhost:5000/api/users"

# Get user ID from the user
user_id = input("Enter user ID: ")

# Make a GET request to retrieve the user by ID
get_user_url = f"{api_url}/{user_id}"
get_response = requests.get(get_user_url)

# Print the retrieved user information
print(get_response.status_code)
print(get_response.json())

# Check if the user retrieval was successful
if get_response.status_code == 200:
    print("User retrieved successfully")
else:
    # Print an error message if user retrieval failed
    print(f"User retrieval failed. Status code: {get_response.status_code}")

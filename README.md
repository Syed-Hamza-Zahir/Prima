# Prima Flask API

Prima is a simple Flask API for user creation and retrieval, featuring a SQLite database and environment variable-based configuration.

## Table of Contents

1. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Server](#running-the-server)
2. [API Endpoints](#api-endpoints)
   - [Create User](#create-user-endpoint)
   - [Get User](#get-user-endpoint)
3. [Request/Response Formats](#requestresponse-formats)
   - [Create User](#create-user-post-apiusers)
   - [Get User](#get-user-get-apiusersuser_id)
4. [Error Handling](#error-handling)
5. [Conclusion](#conclusion)

## Getting Started

### Prerequisites

- Flask
- Flask-SQLAlchemy
- Werkzeug
- SQLAlchemy

### Installation

```bash
git clone https://github.com/Syed-Hamza-Zahir/Prima.git
cd Prima
python -m venv venv
.\venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt

### Running the Server
```bash

cd app
python app.py
```
The server will be running at http://localhost:5000.
```
### Running the Server
```bash

cd app
python app.py
```
The server will be running at http://localhost:5000.

## API Endpoints
### 1. Create User
Endpoint: POST /api/users
Request Format: JSON
Response Format: JSON

### 2. Get User
Endpoint: GET /api/users/{user_id}
Response Format: JSON

### Request/Response Formats
Create User (POST /api/users)
Request Format:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```
Response Format:

```json
{
  "message": "string",
  "user_id": "int"
}
```
Get User (GET /api/users/{user_id})
Response Format:

```json

{
  "user_id": "int",
  "username": "string",
  "email": "string",
}
```
## Examples
### Create User Example
Request:

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123!"
}
```
Response:

```json
{
  "message": "User created successfully",
  "user_id": 1
}
```

### Get User Example
Response:

```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
}
```
## Error Handling
- 400 Bad Request: Invalid input data.
- 404 Not Found: User not found.
- 500 Internal Server Error: Server error.

## Dockerisation

### Building the Docker Image
To build the Docker image for the API server, follow these steps:

1. Ensure you have Docker installed on your machine.
2. Navigate to the root directory of the project.
3. Run the following command:

    ```bash
    docker build -t your-image-name:latest .
    ```

### Running the Docker Container

After building the Docker image, you can run the container with the following command:

```bash
docker run -p 8080:80 --name your-container-name -d your-image-name:latest

# Conclusion
Thank you for using My Flask API! If you have any questions or issues, please contact smhzahir@googlemail.com.
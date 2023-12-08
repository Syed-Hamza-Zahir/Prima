# Prima Flask API

This is a simple Flask API for user creation and retrieval, featuring a SQLite database. It is first complied into a docker image and which is then deployed in a kubernetes cluster in minikube and finally integrated into GitHub Actions CI-CD.

## Table of Contents

1. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Server](#running-the-server)
   - [Testing](#Testing)
2. [API Endpoints](#api-endpoints)
   - [Create User](#create-user-endpoint)
   - [Get User](#get-user-endpoint)
3. [Request/Response Formats](#requestresponse-formats)
   - [Create User](#create-user-post-apiusers)
   - [Get User](#get-user-get-apiusersuser_id)
4. [Password Strength Validation](#Password-Strength-Validation)
5. [Error Handling](#error-handling)
6. [Dockerisation](#dockerisation)
   - [Building the Docker Image](#Building-the-Docker-Image)
   - [Running the Docker Container](#Running-the-Docker-Container)
   - [Testing the Docker Container](#Testing-the-Docker-Container)
7. [Kubernetes Deployment with Minikube](#kubernetes-deployment-with-minikube)
   - [Install Minikube](#install-minikube)
   - [Kubernetes Manifests](#kubernetes-manifests)
      - [Deployment](#deployment)
      - [Service](#service)
      - [Persistent Volume and Persistent Volume Claim](#Persistent-Volume-and-Persistent-Volume-Claim)
   - [Copy Docker Image to Minikube](#copy-docker-image-to-minikube)
      - [Step 1: Save the Docker Image to a Tar File](#step-1-save-the-docker-image-to-a-tar-file)
      - [Step 2: Copy the Tar File to Minikube](#step-2-copy-the-tar-file-to-minikube)
      - [Step 3: Load the Docker Image in Minikube](#step-3-load-the-docker-image-in-minikube)
      - [Step 4: Verify the Loaded Image](#step-4-verify-the-loaded-image)
   - [Apply Manifests](#apply-manifests)
   - [Access the API](#access-the-api)
      - [From inside minikube](#from-inside-minikube)
      - [From local machine](#from-local-machine)
8. [GitHub Actions](#github-actions)
   - [Super-Linter](#super-linter)
9. [Conclusion](#conclusion)

## Getting Started
### Prerequisites

- Flask
- Flask-SQLAlchemy
- Werkzeug
- SQLAlchemy

## Installation

```bash
git clone https://github.com/Syed-Hamza-Zahir/Prima.git
cd Prima/app
python -m venv venv
.\venv\Scripts\activate  # On Windows
```
or 

```bash
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

## Running the Server
```bash
cd app
python app.py
```
The server will be running at http://localhost:8080.

## Testing
To verify the proper functioning of the server, you can use the following methods:

- **Curl Endpoint:**
  ```bash
  curl http://localhost:8080/api/users
  ```
  **Use Scripts:**
Run the provided 'create-user.py' and 'get-user.py' scripts to test the create and retrieve user endpoints.


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
## Password Strength Validation
The app now includes password strength validation during user creation. Passwords must meet the following criteria:

At least 8 characters long.
Contains at least one capital letter.
Contains at least one number.
Contains at least one special character.

### To do: add email validation

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
docker build -t prima:latest .
```

### Running the Docker Container

After building the Docker image, you can run the container with the following command:

```bash
docker run -p 8080:8080 --name prima -d prima:latest
```
### Testing the Docker Container
To verify the proper functioning of the server, you can use the following methods:

- **Curl Endpoint:**
  ```bash
  curl http://localhost:8080/api/users
  ```
  **Use Scripts:**
Run the provided 'create-user.py' and 'get-user.py' scripts to test the create and retrieve user endpoints.

# Kubernetes Deployment with Minikube

## Install Minikube
Ensure that you have Minikube installed on your development machine. You can download and install Minikube from the official website [here](https://minikube.sigs.k8s.io/docs/start/)

## Kubernetes Manifests
### Deployment
I have created a Kubernetes Deployment manifest (deployment.yaml) for the API server. Defined the desired number of replicas and specified the container image to use. 

### Service
I have created a Kubernetes Service manifest (service.yaml) to expose the API server within the cluster. Use the NodePort type to expose it on a port that can be accessed from outside the cluster.

### Persistent Volume and Persistent Volume Claim 
I have implemented data persistence for the API server using Kubernetes Persistent Volumes (PV) and Persistent Volume Claims (PVC). This ensures that data is retained even if the pod is rescheduled or recreated.

I created a Persistent Volume (`persistent-volume.yaml`) to provide storage resources for the API server. The PV is configured with the necessary capacity, access modes, and storage class.

I created a Persistent Volume Claim (`persistent-volume-claim.yaml`) to request storage resources from the Persistent Volume. The PVC specifies the required capacity and references the storage class defined in the PV.

## Copy docker image to minikube 
To copy a local Docker image into the Minikube environment, you can use the docker save and docker load commands:

### Step 1: Save the Docker Image to a Tar File
Run the following command to save your local Docker image to a tar file.
```bash
docker save -o prima.tar prima:latest
```
### Note
There are other ways to load the image if the following doesn't work such as ```docker cp prima.tar [containerID]:/``` the tar image into the minikube docker container and ```docker load -i prima.tar```. 

### Step 2: Copy the Tar File to Minikube
Copy the tar file (local-image.tar) to the Minikube VM. 
```bash
minikube scp local-image.tar minikube:/tmp
```
This command copies the tar file to the /tmp directory inside the Minikube VM:

### Step 3: Load the Docker Image in Minikube
SSH into the Minikube VM and run the following commands to load the Docker image:
```bash
minikube ssh
docker load -i /tmp/local-image.tar
```

### Step 4: Verify the Loaded Image
Check if the image is loaded into Minikube:
```bash
minikube ssh
docker images
```
You should see your locally copied image in the list.

## Apply Manifests
Deploy your API server, PVC, PV and service to the Minikube cluster. Check deployment by verifying that your API server and service resources are running and have the desired configurations.

### Note: Make sure to apply these YAML files in the correct order:

Apply the PersistentVolume (PV) YAML: ```kubectl apply -f pv.yaml```
Apply the PersistentVolumeClaim (PVC) YAML: ```kubectl apply -f pvc.yaml```
Apply the Deployment YAML: ```kubectl apply -f deployment.yaml```
Apply the Service YAML:  ```kubectl apply -f service.yaml```
This order ensures that the PersistentVolume is available before the PersistentVolumeClaim and Deployment are created.

```bash
kubectl get pods
kubectl get deployments
kubectl get service
```

## Access the API
### From inside minikube
Access your Python API server through the Minikube IP address and NodePort. You will need to use Minikube commands to retrieve the IP and port. To access your Python API server deployed on Minikube, you'll need to follow these steps:

Get Minikube IP:
```bash
minikube ip
```
Get NodePort:
```bash
kubectl get services
```
Look for the service associated with your API, and check the PORT(S) column. The NodePort will be listed there.

### From local machine

```bash
minikube service --url flask-api-service
```
Check connectivity as so, or use the 'k8s-create-user.py' from within the minikube container: 
```bash
curl http://[minikubeIP]:[nodePort]/api/users
```

# GitHub Actions

## Super-Linter

Integrate Super-Linter into your GitHub Actions workflow to automatically lint various types of files in your repository.
Create a GitHub Actions workflow YAML file (e.g., `.github/workflows/super-linter.yml`) for example, I've used [this workflow](https://github.com/devopsjourney1/mygitactions/tree/main)
This workflow will run Super-Linter on each push to the main branch.

Conclusion
# Conclusion
Thank you for using My Flask API! If you have any questions or issues, please contact smhzahir@googlemail.com.
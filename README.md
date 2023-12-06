# Prima Flask API

This is a simple Flask API for user creation and retrieval, featuring a SQLite database. It is first complied into a docker image and later deployed in a kubernetes cluster.

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
5. [Dockerization](#dockerization)
6. [Kubernetes Deployment with Minikube](#kubernetes-deployment-with-minikube)
   - [Install Minikube](#install-minikube)
   - [Kubernetes Manifests](#kubernetes-manifests)
      - [Deployment](#deployment)
      - [Service](#service)
   - [Copy Docker Image to Minikube](#copy-docker-image-to-minikube)
      - [Step 1: Save the Docker Image to a Tar File](#step-1-save-the-docker-image-to-a-tar-file)
      - [Step 2: Copy the Tar File to Minikube](#step-2-copy-the-tar-file-to-minikube)
      - [Step 3: Load the Docker Image in Minikube](#step-3-load-the-docker-image-in-minikube)
      - [Step 4: Verify the Loaded Image](#step-4-verify-the-loaded-image)
   - [Apply Manifests](#apply-manifests)
   - [Access the API](#access-the-api)
7. [Conclusion](#conclusion)

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
```
or 

```bash
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### Running the Server
```bash
cd app
python app.py
```
The server will be running at http://localhost:5000.

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
docker run -p 8080:8080 --name your-container-name -d your-image-name:latest
```
# Kubernetes Deployment with Minikube
## Install Minikube
Ensure that you have Minikube installed on your development machine. You can download and install Minikube from the official website [here](https://minikube.sigs.k8s.io/docs/start/)

## Kubernetes Manifests
### Deployment
Create a Kubernetes Deployment manifest (deployment.yaml) for your API server. Define the desired number of replicas and specify the container image to use. Ensure that your API server is exposed on the correct port.

### Service
Create a Kubernetes Service manifest (service.yaml) to expose your API server within the cluster. Use the NodePort type to expose it on a port that can be accessed from outside the cluster.

## Copy docker image to minikube 
To copy a local Docker image into the Minikube environment, you can use the docker save and docker load commands:
# Note
There are other ways to load the image if the following doesn't work. 

# Step 1: Save the Docker Image to a Tar File
Run the following command to save your local Docker image to a tar file.
```bash
docker save -o local-image.tar your-image-name:tag
```
# Note
There are other ways to load the image if the following doesn't work such as ```docker cp``` the tar image into the minikube docker container and ```docker load -i tar image```. 

# Step 2: Copy the Tar File to Minikube
Copy the tar file (local-image.tar) to the Minikube VM. You can use the minikube scp command for this. 
```bash
minikube scp local-image.tar minikube:/tmp
```
This command copies the tar file to the /tmp directory inside the Minikube VM.

# Step 3: Load the Docker Image in Minikube
SSH into the Minikube VM and run the following commands to load the Docker image:
```bash
minikube ssh
docker load -i /tmp/local-image.tar
```

# Step 4: Verify the Loaded Image
Check if the image is loaded into Minikube:
```bash
minikube ssh
docker images
```
You should see your locally copied image in the list.

### Apply Manifests
Deploy your API server and service to the Minikube cluster. Check deployment by verifying that your API server and service resources are running and have the desired configurations.

## Note: Make sure to apply these YAML files in the correct order:

Apply the PersistentVolume (PV) YAML: ```kubectl apply -f pv.yaml```
Apply the PersistentVolumeClaim (PVC) YAML: ```kubectl apply -f pvc.yaml```
Apply the Deployment YAML: ```kubectl apply -f deployment.yaml```
This order ensures that the PersistentVolume is available before the PersistentVolumeClaim and Deployment are created.

```bash
kubectl get pods
kubectl get deployments
kubectl get service
```

### Access the API
Access your Python API server through the Minikube IP address and NodePort. You may need to use Minikube commands to retrieve the IP and port.
To access your Python API server deployed on Minikube, you'll need to follow these steps:

Get Minikube IP:
```bash
minikube ip
```
Get NodePort:
```bash
kubectl get services
```
Look for the service associated with your API, and check the PORT(S) column. The NodePort will be listed there.

Access the API:
Now, you can access your API using the Minikube IP address and NodePort. Run the following command:

```bash
minikube service --url your-api-service
```
Check connectivity as so or use the 'k8s-create-user.py': 
```bash
curl http://127.0.0.1:59219/api/users
```

## TODO:
## NExt, we wait to filesystem between the pods to be in sync. for this create a folder /data/minikube/ in the minikube container

## Create a Persistent Volume (PV):
Define a Persistent Volume that represents the physical storage. For SQLite databases, a ReadWriteOnce access mode might be appropriate.

Apply the PV:
```bash
kubectl apply -f pv.yaml
```
## Create a Persistent Volume Claim (PVC):
Define a Persistent Volume Claim that requests a specific amount of storage. Pods can use PVCs to use storage.

Apply the PVC:

```bash
kubectl apply -f pvc.yaml
```

## Mount the PVC in Pods:
In your deployment YAML, mount the PVC into the desired path in your pods.


Apply the deployment:

```bash
kubectl apply -f deployment.yaml
```

Now, the SQLite database file will be shared among the pods through the PVC. Any changes made to the database by one pod will be visible to other pods sharing the same PVC.

# Conclusion
Thank you for using My Flask API! If you have any questions or issues, please contact smhzahir@googlemail.com.
# Product Similarity Service

This project includes two main components:
1. **FastAPI Application**: Provides an API endpoint to find similar products based on a given product ID.
2. **Streamlit Application**: Provides a user interface to interact with the FastAPI endpoint and display similar products.

## Project Structure

similarity-service-application/
├── app.py
├── SAP_Take_Home_Challenge_Model_Build.py
├── streamlit_app.py
├── requirements.txt
├── Final_cleaned_dataset.csv
├── Dockerfile
├── deployment.yaml
└── service.yaml


## Requirements

Ensure you have the following tools installed:
- Python 3.9 or later
- `pip` (Python package installer)
- Docker (optional, for containerization)
- Kubernetes (optional, for deployment)

## Setup and Running Locally

### 1. Create and Activate a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate```

### 2. Install Dependencies

```bash
pip install -r requirements.txt```

### 3. Run the FastAPI Application
```bash uvicorn app:app --reload --host 127.0.0.1 --port 8000```


### 4. Run the Streamlit Application (in another terminal)
streamlit run streamlit_app.py --server.port 8502 --server.address 127.0.0.1

### 5. Access the Applications
FastAPI: Open your browser and go to http://127.0.0.1:8000.
Streamlit: Open your browser and go to http://127.0.0.1:8502.


Dockerization

Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

COPY Final_cleaned_dataset.csv /app/Final_cleaned_dataset.csv

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8502

# Define environment variable
ENV NAME ProductSimilarityApp

# Run FastAPI and Streamlit apps
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 8502 --server.address 0.0.0.0"]

Build and Run Docker Container
docker build -t similarity-service-application .
docker run -p 8000:8000 -p 8502:8502 similarity-service-application


Kubernetes Deployment
Deployment Configuration (deployment.yaml)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: similarity-service-application
spec:
  replicas: 1
  selector:
    matchLabels:
      app: similarity-service-application
  template:
    metadata:
      labels:
        app: similarity-service-application
    spec:
      containers:
      - name: similarity-service-application
        image: arvindveerelli/similarity-service-application:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        - containerPort: 8502
        resources:
          limits:
            memory: "4Gi"
            cpu: "4"
          requests:
            memory: "4Gi"
            cpu: "4"


Service Configuration (service.yaml)
apiVersion: v1
kind: Service
metadata:
  name: similarity-service-application
spec:
  selector:
    app: similarity-service-application
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
      nodePort: 32000
    - protocol: TCP
      port: 8502
      targetPort: 8502
      nodePort: 32002
  type: NodePort


Apply Kubernetes Configuration

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

Access the Applications
FastAPI: Open your browser and go to http://<node-ip>:32000.
Streamlit: Open your browser and go to http://<node-ip>:32002.

Summary
This README includes the steps and changes needed to integrate and run both the FastAPI and Streamlit applications. The project can be run locally, Dockerized, or deployed using Kubernetes. Follow the instructions for the respective setup and ensure all dependencies are installed correctly.


This README file provides a comprehensive guide on how to set up, run, and deploy the application both locally and using Docker and Kubernetes. You can copy and paste this content into your README.md file.

# AIG200_model_deployment
A cloud-deployed machine learning project that uses a CNN to classify Fashion-MNIST images, served via a containerized REST API on AWS Elastic Beanstalk.

Fashion-MNIST Classifier API
This project demonstrates the deployment of a TensorFlow CNN model that classifies fashion items. The model is served via a REST API built with FastAPI and deployed as a Docker container on AWS Elastic Beanstalk.

Live Prediction Endpoint: http://fashion-api-app-env.eba-bjtp3vk3.us-east-1.elasticbeanstalk.com/predict/

Tech Stack
Model: TensorFlow / Keras (CNN)

API: FastAPI, Uvicorn

Containerization: Docker

Cloud Deployment: AWS Elastic Beanstalk, Amazon ECR

# 1. Local Setup (without Docker)
## Clone this repository
git clone [https://github.com/malhar-39/AIG200_model_deployment]
cd [AIG200_model_deployment]

## Install dependencies
pip install -r requirements.txt

## Run the API server
uvicorn main:app --reload

The API will be available at http://127.0.0.1:8000.

# 2. Running with Docker
## Build the Docker image
docker build -t fashion-api .

## Run the container
docker run -p 8000:8000 fashion-api

The API will be available at http://127.0.0.1:8000.

API Endpoint: /predict/
Method: POST

Description: Receives a 28x28 grayscale image and returns the predicted clothing class.

Request Body:

{
  "image": [[...], [...], ... ] // A 28x28 list of lists containing pixel values
}

Success Response:

{
  "predicted_class": "Pullover",
  "confidence": "0.9985"
}

A client script, test_api.py, is included in the repository to demonstrate how to interact with the API by allowing a user to upload an image.

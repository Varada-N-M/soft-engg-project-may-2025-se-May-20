#!/bin/bash

# Variables
AWS_REGION="us-east-1" # Change to your desired region
ECR_REPO_NAME="your-ecr-repo-name" # Replace with your ECR repository name
BACKEND_IMAGE_TAG="backend:latest"
FRONTEND_IMAGE_TAG="frontend:latest"

# Authenticate Docker with ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query "account" --output text).dkr.ecr.$AWS_REGION.amazonaws.com

# Build Docker images
cd backend

docker build -t $BACKEND_IMAGE_TAG .

cd ../frontend

docker build -t $FRONTEND_IMAGE_TAG .

# Tag Docker images with ECR repository URI
ACCOUNT_ID=$(aws sts get-caller-identity --query "account" --output text)
ECR_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME"

docker tag $BACKEND_IMAGE_TAG $ECR_URI-backend:latest
docker tag $FRONTEND_IMAGE_TAG $ECR_URI-frontend:latest

# Push Docker images to ECR
docker push $ECR_URI-backend:latest
docker push $ECR_URI-frontend:latest

echo "Docker images pushed to ECR repository: $ECR_REPO_NAME"
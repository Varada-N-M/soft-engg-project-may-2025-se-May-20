#!/bin/bash

# Variables
RESOURCE_GROUP="MicrosoftAI-Intellexa" # Replace with your resource group name
APP_SERVICE_PLAN="your-app-service-plan" # Replace with your App Service plan name
WEB_APP_NAME="GrowWise" # Replace with your backend web app name
REGION="East US" # Replace with your Azure region

# Login to Azure
az login

# Create a resource group
az group create --name $RESOURCE_GROUP --location $REGION

# Create an App Service plan
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# Create a Web App for the backend
az webapp create --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --runtime "DOCKER|"

# Configure the Web App to use a Docker container
az webapp config container set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --docker-custom-image-name "your-backend-image" # Replace with your Docker image

# Restart the Web App
az webapp restart --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

echo "Backend deployed to Azure Web App: $WEB_APP_NAME"
#!/bin/bash

# Variables
RESOURCE_GROUP="MicrosoftAI-Intellexa" # Replace with your resource group name
STORAGE_ACCOUNT="yourstorageaccount" # Replace with your storage account name
REGION="East US" # Replace with your Azure region

# Login to Azure
az login

# Create a resource group
az group create --name $RESOURCE_GROUP --location $REGION

# Create a storage account
az storage account create --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --location $REGION --sku Standard_LRS

# Enable static website hosting
az storage blob service-properties update --account-name $STORAGE_ACCOUNT --static-website --index-document index.html --error-document index.html

# Build the frontend
cd frontend
npm install
npm run build

# Upload files to the storage account
az storage blob upload-batch --account-name $STORAGE_ACCOUNT --source dist --destination \$web

echo "Frontend deployed to Azure Storage Static Website: https://$STORAGE_ACCOUNT.z13.web.core.windows.net"
#!/bin/bash

# Variables
BUCKET_NAME="your-s3-bucket-name"
DIST_DIR="dist"

# Build the frontend
npm install
npm run build

# Sync the build directory to S3
aws s3 sync $DIST_DIR s3://$BUCKET_NAME --delete

# Set public read permissions for all files
aws s3 website s3://$BUCKET_NAME/ --index-document index.html --error-document index.html

echo "Frontend deployed to S3 bucket: $BUCKET_NAME"
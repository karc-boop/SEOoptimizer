#!/bin/bash

# Exit on error
set -e

# Load environment variables
source .env.production

# Build and push Docker image
echo "Building and pushing Docker image..."
docker build -t gcr.io/${PROJECT_ID}/seo-optimizer .
docker push gcr.io/${PROJECT_ID}/seo-optimizer

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy seo-optimizer \
    --image gcr.io/${PROJECT_ID}/seo-optimizer \
    --platform managed \
    --region ${LOCATION} \
    --allow-unauthenticated \
    --set-env-vars "DATABASE_URL=${DATABASE_URL},PROJECT_ID=${PROJECT_ID}"

echo "Deployment completed!" 
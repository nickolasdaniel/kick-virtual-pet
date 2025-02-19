#!/bin/bash
# deploy.sh – A sample AWS deployment script
# Make sure to chmod +x deploy.sh before running

# Set variables (replace <aws_account_id> with your actual account ID)
AWS_REGION="us-east-1"
ECR_BACKEND_REPO="kick-virtual-pet-backend"
ECR_FRONTEND_REPO="kick-virtual-pet-frontend"
CLUSTER_NAME="kick-virtual-pet-cluster"
SERVICE_BACKEND="kick-virtual-pet-backend-service"
SERVICE_FRONTEND="kick-virtual-pet-frontend-service"
AWS_ACCOUNT_ID="<aws_account_id>"

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Build and push the backend image
docker build -t $ECR_BACKEND_REPO ./backend
docker tag $ECR_BACKEND_REPO:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/$ECR_BACKEND_REPO:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/$ECR_BACKEND_REPO:latest

# Build and push the frontend image
docker build -t $ECR_FRONTEND_REPO ./frontend
docker tag $ECR_FRONTEND_REPO:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/$ECR_FRONTEND_REPO:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/$ECR_FRONTEND_REPO:latest

# Update ECS services (assumes services are already created and configured)
aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_BACKEND --force-new-deployment --region $AWS_REGION
aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_FRONTEND --force-new-deployment --region $AWS_REGION

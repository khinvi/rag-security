#!/bin/bash
# deploy.sh

# Set variables
IMAGE_NAME="secure-rag"
AWS_REGION="us-west-2"
ECR_REPO_NAME="secure-rag"
STACK_NAME="secure-rag-stack"

# Build Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME:latest .

# Login to ECR
echo "Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Create ECR repository if it doesn't exist
if ! aws ecr describe-repositories --repository-names $ECR_REPO_NAME --region $AWS_REGION > /dev/null 2>&1; then
    echo "Creating ECR repository..."
    aws ecr create-repository --repository-name $ECR_REPO_NAME --region $AWS_REGION
fi

# Tag and push image
echo "Pushing image to ECR..."
docker tag $IMAGE_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:latest

# Deploy CloudFormation stack
echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file aws-deployment.yml \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        OpenAIApiKey=$OPENAI_API_KEY \
        PineconeApiKey=$PINECONE_API_KEY \
        PineconeEnvironment=$PINECONE_ENVIRONMENT \
        PineconeIndex=$PINECONE_INDEX \
    --capabilities CAPABILITY_IAM

# Get the load balancer URL
echo "Deployment complete. Getting load balancer URL..."
LB_URL=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerDNS'].OutputValue" --output text)

echo "Your secure RAG system is deployed at: http://$LB_URL"
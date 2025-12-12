#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Organization Management Service - Kubernetes Deployment${NC}"
echo "=========================================================="

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl is not installed${NC}"
    exit 1
fi

# Check if we're connected to a cluster
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}Error: Not connected to a Kubernetes cluster${NC}"
    echo "Please configure kubectl to connect to your cluster"
    exit 1
fi

echo -e "${GREEN}✓ Connected to Kubernetes cluster${NC}"
echo "Cluster: $(kubectl config current-context)"

# Build Docker image
echo -e "\n${YELLOW}Building Docker image...${NC}"
docker build -t organizationservice:latest .

# For production, you would push to a registry
# docker tag organizationservice:latest your-registry/organization-service:v1.0.0
# docker push your-registry/organization-service:v1.0.0

# Apply Kubernetes configurations
echo -e "\n${YELLOW}Applying Kubernetes configurations...${NC}"

echo "1. Creating namespace..."
kubectl apply -f k8s/namespace.yaml

echo "2. Creating secrets..."
kubectl apply -f k8s/secrets.yaml

echo "3. Creating configmap..."
kubectl apply -f k8s/configmap.yaml

echo "4. Deploying MongoDB..."
kubectl apply -f k8s/mongodb.yaml

# Wait for MongoDB to be ready
echo -e "\n${YELLOW}Waiting for MongoDB to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app=mongodb -n org-management --timeout=300s

echo "5. Deploying application..."
kubectl apply -f k8s/deployment.yaml

echo "6. Creating service..."
kubectl apply -f k8s/service.yaml

echo "7. Setting up autoscaling..."
kubectl apply -f k8s/hpa.yaml

echo "8. Creating storage for backups..."
kubectl apply -f k8s/pvc.yaml

echo "9. Setting up backup job..."
kubectl apply -f k8s/job-backup.yaml

# Wait for application to be ready
echo -e "\n${YELLOW}Waiting for application to be ready...${NC}"
kubectl wait --for=condition=available deployment/organization-service -n org-management --timeout=300s

# Get service information
echo -e "\n${GREEN}✅ Deployment Complete!${NC}"
echo -e "\n${YELLOW}Service Information:${NC}"

# Get ClusterIP service URL
CLUSTER_IP=$(kubectl get svc organization-service -n org-management -o jsonpath='{.spec.clusterIP}')
echo "Cluster IP: $CLUSTER_IP:80"

# Get NodePort service URL
NODE_PORT=$(kubectl get svc organization-service-nodeport -n org-management -o jsonpath='{.spec.ports[0].nodePort}')
echo "NodePort: <any-node-ip>:$NODE_PORT"

# Get pod status
echo -e "\n${YELLOW}Pod Status:${NC}"
kubectl get pods -n org-management

# Get service status
echo -e "\n${YELLOW}Service Status:${NC}"
kubectl get svc -n org-management

echo -e "\n${GREEN}To access the service:${NC}"
echo "1. Cluster internal: http://organization-service.org-management.svc.cluster.local"
echo "2. External via NodePort: http://<node-ip>:$NODE_PORT"
echo "3. API Documentation: Add '/docs' to the URL"
echo "4. Health check: Add '/health' to the URL"

echo -e "\n${YELLOW}To view logs:${NC}"
echo "kubectl logs -f deployment/organization-service -n org-management"

echo -e "\n${YELLOW}To scale the deployment:${NC}"
echo "kubectl scale deployment organization-service --replicas=5 -n org-management"
#!/bin/bash
# Dashboard Deployment Script
# Deploys Dashboard to Full Potential AI server

set -e  # Exit on error

echo "🌐 Full Potential AI - Dashboard Deployment"
echo "=========================================="
echo ""

# Configuration
SERVER="198.54.123.234"
DEPLOY_PATH="/opt/fpai/apps/dashboard"
SERVICE_NAME="dashboard"
PORT=8002

echo "📋 Deployment Configuration:"
echo "   Server: $SERVER"
echo "   Path: $DEPLOY_PATH"
echo "   Port: $PORT"
echo ""

# Step 1: Build Docker image locally
echo "🔨 Step 1: Building Docker image..."
docker build -t fpai-dashboard:latest .
if [ $? -eq 0 ]; then
    echo "   ✅ Docker image built successfully"
else
    echo "   ❌ Docker build failed"
    exit 1
fi
echo ""

# Step 2: Save image to tar
echo "📦 Step 2: Saving Docker image..."
docker save fpai-dashboard:latest -o /tmp/dashboard-image.tar
if [ $? -eq 0 ]; then
    echo "   ✅ Image saved to /tmp/dashboard-image.tar"
else
    echo "   ❌ Failed to save image"
    exit 1
fi
echo ""

# Step 3: Create deployment package
echo "📂 Step 3: Creating deployment package..."
mkdir -p /tmp/dashboard-deploy
cp /tmp/dashboard-image.tar /tmp/dashboard-deploy/
cp docker-compose.yml /tmp/dashboard-deploy/ 2>/dev/null || echo "   ⚠️  No docker-compose.yml found, skipping"
cp .env.example /tmp/dashboard-deploy/.env 2>/dev/null || echo "   ⚠️  No .env.example found, skipping"

# Create server deployment script
cat > /tmp/dashboard-deploy/deploy-on-server.sh << 'SERVERSCRIPT'
#!/bin/bash
# Run this script ON THE SERVER

set -e

echo "🚀 Deploying Dashboard on server..."

# Load the Docker image
echo "📥 Loading Docker image..."
docker load -i dashboard-image.tar
echo "   ✅ Image loaded"

# Stop existing container if running
echo "🛑 Stopping existing container..."
docker stop dashboard 2>/dev/null || true
docker rm dashboard 2>/dev/null || true
echo "   ✅ Old container removed"

# Run new container
echo "🏃 Starting new container..."
docker run -d \
    --name dashboard \
    --restart unless-stopped \
    -p 8002:8002 \
    -e REGISTRY_URL=http://localhost:8000 \
    -e ORCHESTRATOR_URL=http://localhost:8001 \
    fpai-dashboard:latest

if [ $? -eq 0 ]; then
    echo "   ✅ Dashboard started successfully"
else
    echo "   ❌ Failed to start Dashboard"
    exit 1
fi

# Wait for service to be ready
echo "⏳ Waiting for service to be ready..."
sleep 5

# Health check
echo "🏥 Running health check..."
curl -f http://localhost:8002/health || {
    echo "   ❌ Health check failed"
    docker logs dashboard
    exit 1
}
echo "   ✅ Health check passed"

# Show logs
echo ""
echo "📋 Recent logs:"
docker logs --tail 20 dashboard

echo ""
echo "✅ Dashboard deployment complete!"
echo "🌐 Service running at: http://198.54.123.234:8002"
echo "📊 Paradise Progress: http://198.54.123.234:8002/paradise-progress"
SERVERSCRIPT

chmod +x /tmp/dashboard-deploy/deploy-on-server.sh
echo "   ✅ Deployment package ready at /tmp/dashboard-deploy/"
echo ""

# Step 4: Display next steps
echo "=========================================="
echo "✅ Local preparation complete!"
echo ""
echo "📤 Next steps to deploy to server:"
echo ""
echo "   1. Transfer files to server:"
echo "      scp -r /tmp/dashboard-deploy/* root@$SERVER:$DEPLOY_PATH/"
echo ""
echo "   2. SSH to server and run deployment:"
echo "      ssh root@$SERVER"
echo "      cd $DEPLOY_PATH"
echo "      ./deploy-on-server.sh"
echo ""
echo "   3. Verify deployment:"
echo "      curl http://$SERVER:$PORT/health"
echo "      curl http://$SERVER:$PORT/api/paradise-progress"
echo ""
echo "   4. Access Paradise Progress:"
echo "      http://$SERVER:$PORT/paradise-progress"
echo ""
echo "=========================================="
echo ""
echo "🎯 Quick deploy (run these commands):"
echo ""
echo "scp -r /tmp/dashboard-deploy/* root@$SERVER:$DEPLOY_PATH/"
echo "ssh root@$SERVER 'cd $DEPLOY_PATH && ./deploy-on-server.sh'"
echo ""

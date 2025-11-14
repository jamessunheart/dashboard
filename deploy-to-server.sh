#!/bin/bash
# Dashboard Deployment Script
# Run this ON THE SERVER (198.54.123.234)

set -e  # Exit on error

SERVER_USER="root"
SERVER_IP="198.54.123.234"
APP_NAME="dashboard"
DEPLOY_PATH="/opt/fpai/apps/${APP_NAME}"
PORT=8002

echo "=========================================="
echo "  FPAI Dashboard Deployment"
echo "=========================================="
echo ""

# Check if running on server
if [[ "$(hostname -I | grep -c '198.54.123.234')" -eq 0 ]]; then
    echo "⚠️  This script should be run ON THE SERVER"
    echo "Please SSH to the server first:"
    echo "  ssh root@198.54.123.234"
    echo "  cd /opt/fpai/apps/dashboard"
    echo "  ./deploy-to-server.sh"
    exit 1
fi

echo "[1/8] Creating deployment directory..."
mkdir -p ${DEPLOY_PATH}
cd ${DEPLOY_PATH}

echo "[2/8] Pulling latest code from GitHub..."
if [ -d ".git" ]; then
    git pull origin main
else
    git clone https://github.com/fpai-track-b/dashboard.git .
fi

echo "[3/8] Stopping existing container (if running)..."
docker stop fpai-${APP_NAME} 2>/dev/null || true
docker rm fpai-${APP_NAME} 2>/dev/null || true

echo "[4/8] Building Docker image..."
docker build -t fpai-${APP_NAME}:latest .

echo "[5/8] Starting new container..."
docker run -d \
    --name fpai-${APP_NAME} \
    -p ${PORT}:${PORT} \
    -e REGISTRY_URL=http://198.54.123.234:8000 \
    -e ORCHESTRATOR_URL=http://198.54.123.234:8001 \
    -e PORT=${PORT} \
    --restart unless-stopped \
    fpai-${APP_NAME}:latest

echo "[6/8] Waiting for service to start..."
sleep 5

echo "[7/8] Verifying health..."
HEALTH_URL="http://localhost:${PORT}/health"
if curl -f -s ${HEALTH_URL} > /dev/null; then
    echo "✅ Service is healthy!"
    curl -s ${HEALTH_URL} | python3 -m json.tool
else
    echo "❌ Health check failed!"
    echo "Checking logs..."
    docker logs fpai-${APP_NAME} --tail 50
    exit 1
fi

echo "[8/8] Checking registration with Registry..."
sleep 3
curl -s http://localhost:8000/droplets | python3 -m json.tool | grep -A 5 "dashboard" || echo "Not yet registered (will register on next heartbeat)"

echo ""
echo "=========================================="
echo "  ✅ Dashboard Deployment Complete!"
echo "=========================================="
echo ""
echo "Access at:"
echo "  - Local: http://localhost:${PORT}"
echo "  - Public: http://198.54.123.234:${PORT}"
echo ""
echo "Logs:"
echo "  docker logs -f fpai-${APP_NAME}"
echo ""
echo "🌐⚡💎"

#!/bin/bash
# One-Command Deploy to Live Server
# Usage: ./deploy-live.sh

set -e

SERVER="198.54.123.234"
REMOTE_PATH="/opt/fpai/apps/dashboard"

echo "🌐 Full Potential AI - Dashboard Deploy"
echo "========================================"
echo "📍 Server: $SERVER:8002"
echo ""

# Step 1: Sync files
echo "📤 Step 1: Syncing files to server..."
rsync -avz --exclude .venv --exclude __pycache__ --exclude .git --exclude htmlcov \
  ~/Development/dashboard/ \
  root@$SERVER:$REMOTE_PATH/

if [ $? -eq 0 ]; then
    echo "   ✅ Files synced"
else
    echo "   ❌ Sync failed"
    exit 1
fi
echo ""

# Step 2: Deploy on server
echo "🚀 Step 2: Deploying on server..."
ssh root@$SERVER << 'ENDSSH'
cd /opt/fpai/apps/dashboard

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "   📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate and install dependencies
source .venv/bin/activate
echo "   📦 Installing dependencies..."
pip install -q -r requirements.txt

# Create systemd service if it doesn't exist
if [ ! -f "/etc/systemd/system/dashboard.service" ]; then
    echo "   ⚙️  Creating systemd service..."
    cat > /etc/systemd/system/dashboard.service << 'EOF'
[Unit]
Description=Full Potential AI Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/fpai/apps/dashboard
Environment="PATH=/opt/fpai/apps/dashboard/.venv/bin"
ExecStart=/opt/fpai/apps/dashboard/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8002
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
    systemctl enable dashboard
fi

# Restart service
echo "   🔄 Restarting service..."
systemctl restart dashboard

# Wait a moment for startup
sleep 3

# Check status
if systemctl is-active --quiet dashboard; then
    echo "   ✅ Service is running"
else
    echo "   ❌ Service failed to start"
    systemctl status dashboard
    exit 1
fi

# Health check
echo "   🏥 Running health check..."
if curl -f -s http://localhost:8002/health > /dev/null; then
    echo "   ✅ Health check passed"
else
    echo "   ❌ Health check failed"
    journalctl -u dashboard -n 20
    exit 1
fi

echo ""
echo "📊 Service Status:"
systemctl status dashboard --no-pager -l

ENDSSH

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Deployment successful!"
    echo ""
    echo "🌐 Dashboard is live at:"
    echo "   http://198.54.123.234:8002"
    echo ""
    echo "📊 Paradise Progress:"
    echo "   http://198.54.123.234:8002/paradise-progress"
    echo ""
    echo "🏥 Health Check:"
    curl -s http://198.54.123.234:8002/health | python3 -m json.tool
    echo ""
    echo "📈 Progress Metrics:"
    curl -s http://198.54.123.234:8002/api/paradise-progress | python3 -m json.tool
    echo ""
    echo "=========================================="
    echo ""
    echo "🎯 Ready to point your domain!"
    echo "   DNS A Record: dashboard.fullpotential.ai → 198.54.123.234"
    echo ""
else
    echo "❌ Deployment failed"
    exit 1
fi

#!/bin/bash
# Run these commands ON THE SERVER (198.54.123.234)
# Copy this entire script and run it

set -e

echo "🌐 Deploying Full Potential AI Dashboard"
echo "========================================"
echo ""

# Navigate to apps directory
cd /opt/fpai/apps

# Clone or update dashboard
if [ -d "dashboard" ]; then
    echo "📂 Dashboard directory exists, updating..."
    cd dashboard
    git pull || echo "⚠️  Git pull failed, continuing..."
else
    echo "📥 Cloning dashboard from GitHub..."
    # Try to clone - if it fails, we'll create manually
    git clone https://github.com/jamessunheart/dashboard.git || {
        echo "⚠️  Clone failed, creating directory manually..."
        mkdir -p dashboard
        cd dashboard
    }
fi

cd /opt/fpai/apps/dashboard

# Create virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.1
pydantic==2.5.0
pydantic-settings==2.1.0
jinja2==3.1.2
python-multipart==0.0.6
EOF

pip install -q -r requirements.txt

# Create systemd service
echo "⚙️  Creating systemd service..."
cat > /etc/systemd/system/dashboard.service << 'EOF'
[Unit]
Description=Full Potential AI Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/fpai/apps/dashboard
Environment="PATH=/opt/fpai/apps/dashboard/.venv/bin"
Environment="REGISTRY_URL=http://localhost:8000"
Environment="ORCHESTRATOR_URL=http://localhost:8001"
ExecStart=/opt/fpai/apps/dashboard/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8002
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload

# Enable service
systemctl enable dashboard

# Restart service
echo "🔄 Starting dashboard service..."
systemctl restart dashboard

# Wait for startup
sleep 3

# Check status
echo ""
echo "📊 Service Status:"
systemctl status dashboard --no-pager -l | head -20

# Health check
echo ""
echo "🏥 Health Check:"
if curl -f -s http://localhost:8002/health > /dev/null 2>&1; then
    echo "✅ Dashboard is running!"
    curl -s http://localhost:8002/health | python3 -m json.tool
else
    echo "❌ Health check failed"
    echo "Checking logs:"
    journalctl -u dashboard -n 30 --no-pager
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Dashboard Deployed Successfully!"
echo ""
echo "🌐 Access URLs:"
echo "   http://198.54.123.234:8002/"
echo "   http://198.54.123.234:8002/paradise-progress"
echo "   http://198.54.123.234:8002/live-system"
echo ""
echo "📊 API:"
echo "   http://198.54.123.234:8002/api/paradise-progress"
echo ""
echo "🔧 Service Management:"
echo "   systemctl status dashboard"
echo "   systemctl restart dashboard"
echo "   journalctl -u dashboard -f"
echo ""
echo "=========================================="

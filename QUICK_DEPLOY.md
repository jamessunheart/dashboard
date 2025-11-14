# Dashboard - Quick Deployment Guide

## Deploy to 198.54.123.234:8002

### Option A: Direct File Deploy (Fastest - No Docker)

**Step 1: Copy files to server**
```bash
# From your local machine
rsync -avz --exclude .venv --exclude __pycache__ --exclude .git \
  ~/Development/dashboard/ \
  root@198.54.123.234:/opt/fpai/apps/dashboard/
```

**Step 2: SSH to server and deploy**
```bash
ssh root@198.54.123.234

# Navigate to dashboard
cd /opt/fpai/apps/dashboard

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service (one-time setup)
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

# Enable and start service
systemctl daemon-reload
systemctl enable dashboard
systemctl start dashboard

# Check status
systemctl status dashboard

# View logs
journalctl -u dashboard -f
```

**Step 3: Verify**
```bash
# Health check
curl http://localhost:8002/health

# Paradise progress
curl http://localhost:8002/api/paradise-progress

# From your local machine
curl http://198.54.123.234:8002/paradise-progress
```

---

### Option B: Docker Deploy (If Docker available on server)

**Step 1: Copy files to server**
```bash
rsync -avz ~/Development/dashboard/ \
  root@198.54.123.234:/opt/fpai/apps/dashboard/
```

**Step 2: Build and run on server**
```bash
ssh root@198.54.123.234
cd /opt/fpai/apps/dashboard

# Build image
docker build -t fpai-dashboard:latest .

# Stop old container
docker stop dashboard 2>/dev/null || true
docker rm dashboard 2>/dev/null || true

# Run new container
docker run -d \
  --name dashboard \
  --restart unless-stopped \
  -p 8002:8002 \
  -e REGISTRY_URL=http://localhost:8000 \
  -e ORCHESTRATOR_URL=http://localhost:8001 \
  fpai-dashboard:latest

# Check logs
docker logs -f dashboard
```

---

### Option C: Quick Update (After initial deploy)

```bash
# Just copy changed files and restart
rsync -avz --exclude .venv --exclude __pycache__ \
  ~/Development/dashboard/ \
  root@198.54.123.234:/opt/fpai/apps/dashboard/

ssh root@198.54.123.234 'systemctl restart dashboard'
```

---

## Verification Checklist

After deployment, verify:

- [ ] Health endpoint: http://198.54.123.234:8002/health
- [ ] Paradise Progress: http://198.54.123.234:8002/paradise-progress
- [ ] Live System: http://198.54.123.234:8002/live-system
- [ ] Home page: http://198.54.123.234:8002/
- [ ] API endpoint: http://198.54.123.234:8002/api/paradise-progress

---

## Point Domain

Once deployed and verified, point your domain:

**DNS A Record:**
```
dashboard.fullpotential.ai  →  198.54.123.234
```

**Or subdomain:**
```
progress.fullpotential.ai  →  198.54.123.234
```

Then access via: `http://dashboard.fullpotential.ai:8002/paradise-progress`

*(For HTTPS and no port number, you'll need Proxy Manager - Phase 2 Priority #2!)*

---

## Troubleshooting

**Service won't start:**
```bash
systemctl status dashboard
journalctl -u dashboard -n 50
```

**Port already in use:**
```bash
lsof -i :8002
kill -9 <PID>
```

**Dependencies missing:**
```bash
cd /opt/fpai/apps/dashboard
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Service Management

```bash
# Start
systemctl start dashboard

# Stop
systemctl stop dashboard

# Restart
systemctl restart dashboard

# Status
systemctl status dashboard

# Logs (live)
journalctl -u dashboard -f

# Logs (last 100 lines)
journalctl -u dashboard -n 100
```

---

**Ready to deploy!** 🚀

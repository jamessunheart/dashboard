# Dashboard Deployment Guide

## ✅ What's Been Done

The Dashboard (Droplet #2) is **100% complete** and ready to deploy:

- ✅ Full UDC-compliant backend (FastAPI)
- ✅ Beautiful marketing frontend (HTML/CSS/JS)
- ✅ Live system integration (Registry + Orchestrator)
- ✅ Tests written (pytest)
- ✅ Docker configuration
- ✅ Deployment script
- ✅ Local git repository initialized and committed

## 🚀 Next Steps (For You)

### Step 1: Create GitHub Repository

1. Go to https://github.com/fpai-track-b
2. Click "New repository"
3. Name: `dashboard`
4. Visibility: Public
5. **Do NOT initialize** with README (we have one)
6. Click "Create repository"

### Step 2: Push Code to GitHub

```bash
cd ~/Development/dashboard
git remote add origin https://github.com/fpai-track-b/dashboard.git
git push -u origin main
```

### Step 3: Deploy to Server

**Option A: On the server (recommended):**

```bash
# SSH to server
ssh root@198.54.123.234

# Create deployment directory
mkdir -p /opt/fpai/apps/dashboard
cd /opt/fpai/apps/dashboard

# Clone the repository
git clone https://github.com/fpai-track-b/dashboard.git .

# Run deployment script
chmod +x deploy-to-server.sh
./deploy-to-server.sh
```

**Option B: Manual deployment:**

```bash
# SSH to server
ssh root@198.54.123.234

# Navigate to deployment path
cd /opt/fpai/apps
git clone https://github.com/fpai-track-b/dashboard.git
cd dashboard

# Build and run
docker build -t fpai-dashboard:latest .

docker run -d \
  --name fpai-dashboard \
  -p 8002:8002 \
  -e REGISTRY_URL=http://198.54.123.234:8000 \
  -e ORCHESTRATOR_URL=http://198.54.123.234:8001 \
  --restart unless-stopped \
  fpai-dashboard:latest

# Verify
curl http://localhost:8002/health
```

### Step 4: Verify Deployment

1. **Check health:**
   ```bash
   curl http://198.54.123.234:8002/health
   ```

2. **Check registration with Registry:**
   ```bash
   curl http://198.54.123.234:8000/droplets | grep dashboard
   ```

3. **Visit in browser:**
   - Home: http://198.54.123.234:8002
   - Live System: http://198.54.123.234:8002/live-system
   - Sacred Loop: http://198.54.123.234:8002/sacred-loop

4. **Run server health monitor:**
   ```bash
   cd ~/Development
   ./fpai-ops/server-health-monitor.sh
   ```
   Should show 3 services online: Registry, Orchestrator, Dashboard

### Step 5: (Future) Set Up Domain

When you're ready to point fullpotential.ai to the Dashboard:

1. Update DNS A record: `fullpotential.ai` → `198.54.123.234`
2. Install Nginx/Caddy on server for reverse proxy
3. Configure SSL certificate (Let's Encrypt)
4. Proxy port 80/443 → port 8002

OR wait for Droplet #3 (Proxy Manager) to automate this.

## 📊 What You'll See

Once deployed, the Dashboard will:

- ✅ Register itself with Registry automatically
- ✅ Send heartbeat every 60 seconds
- ✅ Display live status of Registry + Orchestrator
- ✅ Auto-update every 30 seconds
- ✅ Show all marketing pages
- ✅ Be visible at http://198.54.123.234:8002

## 🔧 Troubleshooting

**Dashboard not starting:**
```bash
docker logs fpai-dashboard
```

**Not registering with Registry:**
- Check Registry is running: `curl http://198.54.123.234:8000/health`
- Wait 60 seconds for first heartbeat
- Check logs: `docker logs fpai-dashboard | grep -i registry`

**Frontend not loading:**
- Check port 8002 is accessible
- Try: `curl http://localhost:8002` from server
- Check Docker container is running: `docker ps | grep dashboard`

**Status not updating:**
- Check browser console for JavaScript errors
- Verify API endpoint works: `curl http://198.54.123.234:8002/api/system/status`

## 📝 File Structure

```
dashboard/
├── app/
│   ├── main.py                      # FastAPI application
│   ├── config.py                    # Configuration
│   ├── models.py                    # Data models
│   ├── routers/
│   │   ├── udc.py                   # UDC endpoints
│   │   └── api.py                   # API endpoints
│   ├── services/
│   │   ├── registry_client.py       # Registry integration
│   │   └── orchestrator_client.py   # Orchestrator integration
│   ├── static/
│   │   ├── css/style.css            # Styles
│   │   └── js/main.js               # Live updates
│   └── templates/
│       ├── base.html                # Base template
│       ├── home.html                # Home page
│       ├── sacred-loop.html         # Sacred Loop page
│       ├── live-system.html         # Live system page
│       ├── how-it-works.html        # Architecture page
│       └── get-involved.html        # Get involved page
├── test/                            # Tests
├── Dockerfile                       # Docker configuration
├── docker-compose.yml               # Docker Compose
├── requirements.txt                 # Python dependencies
├── deploy-to-server.sh             # Deployment script
└── README.md                        # Documentation
```

## ✨ Success Criteria

- ✅ Health endpoint responding
- ✅ Registered with Registry
- ✅ All 5 pages loading
- ✅ Live status updating every 30s
- ✅ Responsive design working
- ✅ Shows Registry + Orchestrator online

---

**You're ready to go live!** 🚀

Once deployed, you'll have a public-facing website that:
- Explains your vision
- Shows the system alive
- Attracts users and investors
- Demonstrates real, operational technology

🌐⚡💎

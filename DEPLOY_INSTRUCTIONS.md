# Dashboard - Deploy to Server

## Quick Deploy Package Created!

**Package location:** `~/Development/dashboard-deploy.tar.gz`

---

## Deployment Steps

### Option A: Upload and Deploy (If you have SSH access)

**1. Upload the package:**
```bash
scp ~/Development/dashboard-deploy.tar.gz root@198.54.123.234:/tmp/
```

**2. SSH to server:**
```bash
ssh root@198.54.123.234
```

**3. Extract and deploy:**
```bash
# Create directory
mkdir -p /opt/fpai/apps/dashboard

# Extract
cd /opt/fpai/apps
tar -xzf /tmp/dashboard-deploy.tar.gz

# Navigate to dashboard
cd /opt/fpai/apps/dashboard

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service
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

# Enable and start
systemctl daemon-reload
systemctl enable dashboard
systemctl start dashboard

# Check status
systemctl status dashboard

# Verify
curl http://localhost:8002/health
curl http://localhost:8002/api/paradise-progress
```

---

### Option B: Manual File Upload (If using FTP/Panel)

**1. Download the dashboard folder:**
Location: `~/Development/dashboard/`

**2. Upload to server:**
- Upload all files to: `/opt/fpai/apps/dashboard/`
- Exclude: `.venv/`, `__pycache__/`, `.git/`

**3. On server, run:**
```bash
cd /opt/fpai/apps/dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8002
```

---

### Option C: Direct Server Copy (If you're ON the server)

**If you have the code on the server already:**

```bash
# Navigate to dashboard
cd /opt/fpai/apps/dashboard

# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run directly (for testing)
uvicorn app.main:app --host 0.0.0.0 --port 8002

# Or create service (for production)
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
systemctl start dashboard
```

---

## Verification

Once deployed, verify:

**From the server:**
```bash
curl http://localhost:8002/health
curl http://localhost:8002/api/paradise-progress
```

**From anywhere:**
```bash
curl http://198.54.123.234:8002/health
curl http://198.54.123.234:8002/paradise-progress
```

**In your browser:**
- http://198.54.123.234:8002/paradise-progress
- http://198.54.123.234:8002/live-system
- http://198.54.123.234:8002/

---

## Success Checklist

- [ ] Files uploaded to /opt/fpai/apps/dashboard/
- [ ] Virtual environment created and dependencies installed
- [ ] Service running on port 8002
- [ ] Health check returns OK
- [ ] Paradise Progress page loads in browser
- [ ] Live metrics showing 18% progress

---

## Point Your Domain

Once verified, add DNS record:

```
A Record: dashboard.fullpotential.ai → 198.54.123.234
```

Access at: `http://dashboard.fullpotential.ai:8002/paradise-progress`

---

**Paradise is ready to go live!** 🌐✨

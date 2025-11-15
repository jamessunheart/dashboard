# Secure Deployment Instructions - Dashboard

**Generated:** 2025-11-14
**Service:** Dashboard (Droplet #2)
**Target Server:** 198.54.123.234
**Security Model:** Script review + manual execution

---

## Security Approach

This deployment uses a **review-then-execute** model:
1. ✅ I generate the deployment script
2. ✅ You review it for security
3. ✅ You execute it with your credentials
4. ✅ Full audit trail maintained

**Benefits:**
- No automated SSH access required
- You maintain full control
- Clear, auditable steps
- Secure by design

---

## Deployment Steps

### Step 1: Copy Script to Server

```bash
# From your local machine
scp dashboard/DEPLOY_TO_SERVER_MANUAL.sh root@198.54.123.234:/root/
```

### Step 2: Review the Script

```bash
# On the server
ssh root@198.54.123.234
cat /root/DEPLOY_TO_SERVER_MANUAL.sh
```

**Review checklist:**
- [ ] No suspicious commands
- [ ] Paths look correct (/opt/fpai/apps/dashboard)
- [ ] Ports are correct (8002)
- [ ] GitHub repo URL is correct
- [ ] Service configuration is appropriate

### Step 3: Execute Deployment

```bash
# On the server (after review)
bash /root/DEPLOY_TO_SERVER_MANUAL.sh
```

The script will:
1. Create /opt/fpai/apps/dashboard
2. Clone from GitHub
3. Set up Python venv
4. Install dependencies
5. Run tests (blocks on failure)
6. Create systemd service
7. Start service
8. Verify health

### Step 4: Verify Deployment

```bash
# Check service status
systemctl status fpai-dashboard

# View logs
journalctl -u fpai-dashboard -n 50

# Test health endpoint
curl http://localhost:8002/health

# Test from external
curl http://198.54.123.234:8002/health
```

### Step 5: Verify with Health Monitor

```bash
# From your local machine
./fpai-ops/server-health-monitor.sh
```

Should show:
```
Registry        🟢 ONLINE
Orchestrator    🟢 ONLINE
Dashboard       🟢 ONLINE
System Health: 100% (3/3 services online)
```

---

## What Was Built

**DEPLOY_TO_SERVER_MANUAL.sh** - Secure, reviewable deployment script
- 8-step automated process
- Health verification
- Rollback capability (backup created)
- Systemd service integration

**Updated server-health-monitor.sh**
- Now monitors Dashboard on port 8002
- Tracks 3/3 services

---

## Rollback Procedure

If deployment fails or issues occur:

```bash
# On the server
cd /opt/fpai/apps

# List backups
ls -la | grep dashboard-backup

# Restore from backup
systemctl stop fpai-dashboard
rm -rf dashboard
mv dashboard-backup-YYYYMMDD-HHMMSS dashboard
systemctl start fpai-dashboard
```

---

## Service Management

```bash
# Start service
systemctl start fpai-dashboard

# Stop service
systemctl stop fpai-dashboard

# Restart service
systemctl restart fpai-dashboard

# View logs (live)
journalctl -u fpai-dashboard -f

# View logs (last 100 lines)
journalctl -u fpai-dashboard -n 100
```

---

## Endpoints (After Deployment)

### UDC Endpoints
- `http://198.54.123.234:8002/health` - Health check
- `http://198.54.123.234:8002/capabilities` - Capabilities
- `http://198.54.123.234:8002/state` - Current state
- `http://198.54.123.234:8002/dependencies` - Dependencies
- `http://198.54.123.234:8002/message` - Messaging endpoint

### Application Pages
- `http://198.54.123.234:8002/` - Home
- `http://198.54.123.234:8002/live-system` - Live system visualization
- `http://198.54.123.234:8002/sacred-loop` - Sacred Loop explanation
- `http://198.54.123.234:8002/how-it-works` - Architecture docs
- `http://198.54.123.234:8002/get-involved` - Recruitment

---

## Troubleshooting

### Service won't start
```bash
# Check logs for errors
journalctl -u fpai-dashboard -n 50 --no-pager

# Check if port is in use
netstat -tulpn | grep 8002

# Check Python/dependencies
cd /opt/fpai/apps/dashboard
source .venv/bin/activate
python --version
pip list
```

### Health check fails
```bash
# Test locally on server
curl -v http://localhost:8002/health

# Check if process is running
ps aux | grep uvicorn

# Check systemd status
systemctl status fpai-dashboard
```

### Can't connect from external
```bash
# Check firewall
ufw status
ufw allow 8002/tcp

# Check if service is listening on 0.0.0.0
netstat -tulpn | grep 8002
```

---

## Next Steps After Deployment

1. ✅ Verify all UDC endpoints respond correctly
2. ✅ Check live system visualization works
3. ✅ Confirm integration with Registry/Orchestrator
4. ✅ Run full health monitor check
5. ✅ Update MEMORY/CURRENT_STATE.md

---

## Security Notes

- Script creates systemd service running as root (review if this fits your security model)
- No secrets stored in the script
- All code from GitHub (SSOT)
- Systemd manages process lifecycle
- Logs available via journalctl

---

**Ready to deploy securely. You maintain full control.**

🌐⚡💎

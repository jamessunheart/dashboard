# GitHub Actions Setup Guide

**Automated CI/CD Pipeline for Dashboard Deployment**

---

## 🎯 What This Does

Every time you (or Claude Code) push to the `main` branch:

1. ✅ **Runs all tests** - Ensures code quality
2. 🏗️ **Builds Docker image** - On the server
3. 🚀 **Deploys automatically** - Zero manual intervention
4. ✔️ **Verifies health** - Confirms deployment succeeded
5. 🔄 **Rolls back if failed** - Automatic recovery
6. 📢 **Notifies you** - Success or failure

**Result:** Push to GitHub → Dashboard auto-deploys to server!

---

## 🔑 One-Time Setup (5 minutes)

### Step 1: Generate SSH Key for GitHub Actions

On your **local machine**, run:

```bash
# Generate a new SSH key (no passphrase)
ssh-keygen -t ed25519 -C "github-actions-dashboard" -f ~/.ssh/github-actions-dashboard

# Display the private key (you'll copy this)
cat ~/.ssh/github-actions-dashboard

# Display the public key
cat ~/.ssh/github-actions-dashboard.pub
```

### Step 2: Add Public Key to Server

SSH to your server and add the public key:

```bash
# SSH to server
ssh root@198.54.123.234

# Add public key to authorized_keys
echo "YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys

# Verify permissions
chmod 600 ~/.ssh/authorized_keys
```

### Step 3: Add Private Key to GitHub Secrets

1. Go to: https://github.com/fpai-track-b/dashboard/settings/secrets/actions

2. Click **"New repository secret"**

3. **Name:** `SSH_PRIVATE_KEY`

4. **Value:** Paste the entire private key content from `~/.ssh/github-actions-dashboard`
   - Include the `-----BEGIN OPENSSH PRIVATE KEY-----` header
   - Include the `-----END OPENSSH PRIVATE KEY-----` footer

5. Click **"Add secret"**

---

## ✅ Verify Setup

### Test the Workflow

1. **Make a small change** to any file (or just trigger manually):
   ```bash
   cd ~/Development/dashboard
   echo "# Test" >> README.md
   git add README.md
   git commit -m "Test GitHub Actions deployment"
   git push origin main
   ```

2. **Watch the workflow:**
   - Go to: https://github.com/fpai-track-b/dashboard/actions
   - You'll see the workflow running
   - Green checkmark = success!

3. **Verify deployment:**
   ```bash
   curl http://198.54.123.234:8002/health
   ```

---

## 🚀 How to Use

### Automatic Deployment (Default)

Just push to main:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

**GitHub Actions automatically:**
- Runs tests
- Deploys to server
- Verifies health
- Notifies you of result

### Manual Deployment

Trigger manually from GitHub:
1. Go to: https://github.com/fpai-track-b/dashboard/actions
2. Select "Deploy Dashboard to Server"
3. Click "Run workflow"
4. Choose branch (main)
5. Click "Run workflow"

---

## 📊 Workflow Steps Explained

```
┌─────────────────────────────────────────────────┐
│  1. Test Job                                     │
│     • Checkout code                              │
│     • Setup Python 3.11                          │
│     • Install dependencies                       │
│     • Run pytest                                 │
│     • ✅ Must pass to continue                   │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  2. Deploy Job (only if tests pass)             │
│     • Setup SSH connection                       │
│     • Create backup on server                    │
│     • Pull latest code                           │
│     • Stop old container                         │
│     • Build new Docker image                     │
│     • Start new container                        │
│     • Verify health endpoint                     │
│     • Check Registry registration                │
│     • If fails → Rollback to backup              │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  3. Post-Deploy Job                              │
│     • Display deployment status                  │
│     • Show next steps                            │
└─────────────────────────────────────────────────┘
```

---

## 🔄 Rollback Capability

**Automatic Rollback:**
- If deployment fails, automatically restores last working version
- Uses the backup created before deployment
- Brings service back online quickly

**Manual Rollback:**
If you need to rollback manually:

```bash
# SSH to server
ssh root@198.54.123.234

cd /opt/fpai/apps/dashboard

# List available backups
ls -lh backup-*.tar.gz

# Restore specific backup
BACKUP=backup-20251114-120000.tar.gz
tar -xzf $BACKUP

# Rebuild and restart
docker stop fpai-dashboard
docker rm fpai-dashboard
docker build -t fpai-dashboard:latest .
docker run -d --name fpai-dashboard -p 8002:8002 \
  -e REGISTRY_URL=http://198.54.123.234:8000 \
  -e ORCHESTRATOR_URL=http://198.54.123.234:8001 \
  --restart unless-stopped fpai-dashboard:latest
```

---

## 🐛 Troubleshooting

### Workflow Fails at "Setup SSH"

**Issue:** SSH key not configured properly

**Fix:**
1. Verify secret exists: GitHub repo → Settings → Secrets → SSH_PRIVATE_KEY
2. Verify public key on server: `cat ~/.ssh/authorized_keys`
3. Test SSH manually: `ssh -i ~/.ssh/github-actions-dashboard root@198.54.123.234`

### Workflow Fails at "Run Tests"

**Issue:** Tests failing

**Fix:**
1. Run tests locally: `pytest test/ -v`
2. Fix failing tests
3. Commit and push fix

### Workflow Fails at "Verify deployment"

**Issue:** Service not responding

**Fix:**
1. SSH to server
2. Check logs: `docker logs fpai-dashboard`
3. Check container status: `docker ps -a | grep dashboard`
4. Manual rollback if needed (see above)

### Container Won't Start

**Issue:** Docker build or runtime error

**Fix:**
1. Check workflow logs for build errors
2. SSH to server and check: `docker logs fpai-dashboard`
3. Verify environment variables are set correctly
4. Check port 8002 isn't already in use: `netstat -tlnp | grep 8002`

---

## 🎯 Future Enhancements

### Add Slack/Discord Notifications
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Add Performance Testing
```yaml
- name: Run performance tests
  run: |
    pip install locust
    locust -f tests/performance.py --headless
```

### Add Multiple Environments
```yaml
on:
  push:
    branches:
      - main        # → Production
      - develop     # → Staging
```

---

## ✅ Benefits

**Before GitHub Actions:**
- Claude Code writes code
- Manual git push
- You SSH to server
- You run deployment commands
- You verify it worked
- **Total time:** 5-10 minutes manual work

**After GitHub Actions:**
- Claude Code writes code
- Auto git push
- **Everything else happens automatically**
- You get notified when done
- **Total time:** 0 minutes manual work

**Time saved per deployment:** 5-10 minutes
**Deployments per week:** ~10
**Total time saved:** 1+ hour/week

---

## 🔐 Security Notes

- ✅ SSH key is stored as GitHub Secret (encrypted)
- ✅ Key is only loaded during workflow execution
- ✅ Key is deleted after workflow completes
- ✅ Only accessible to repository collaborators
- ✅ Automatic backups before every deployment
- ✅ Automatic rollback on failure

---

## 📝 Summary

**Setup:** 5 minutes one-time configuration
**Usage:** Fully automatic on every push
**Reliability:** Tests → Deploy → Verify → Rollback if needed
**Time saved:** 1+ hour/week

**You now have enterprise-grade CI/CD for your dashboard!** 🎉

---

**Next:** Apply this same workflow to all future droplets (Registry, Orchestrator, Proxy Manager, etc.)

🌐⚡💎

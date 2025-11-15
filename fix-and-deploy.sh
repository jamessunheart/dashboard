#!/bin/bash
# One-command fix and deploy

echo "🔧 Fixing and deploying Command Center..."

# SSH and run all commands
ssh root@198.54.123.234 << 'ENDSSH'
cd /root/dashboard
git remote set-url origin https://github.com/jamessunheart/fpai-dashboard.git
git fetch origin
git reset --hard origin/main
ls app/templates/command-center.html && echo "✅ Files found!" || echo "❌ Files missing"
docker rm -f fpai-dashboard
docker-compose up -d --build
sleep 5
curl -s http://localhost:8002/command-center | grep -q "Command Center" && echo "✅ Command Center is LIVE!" || echo "❌ Still not found"
ENDSSH

echo ""
echo "🎉 Done! Check: http://198.54.123.234/command-center"

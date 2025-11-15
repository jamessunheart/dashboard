#!/bin/bash
# Deploy Full Potential Membership to dashboard.fullpotential.com
# Run this ON THE SERVER (198.54.123.234)

set -e

echo "🚀 Deploying Full Potential Membership Platform..."
echo ""

# Navigate to dashboard directory
cd /root/dashboard || exit 1

# Pull latest code
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Stop existing container
echo "🛑 Stopping existing dashboard..."
docker-compose down 2>/dev/null || true

# Rebuild and start
echo "🔨 Building and starting dashboard..."
docker-compose up -d --build

# Wait for startup
echo "⏳ Waiting for dashboard to start..."
sleep 5

# Check health
echo "🏥 Checking health..."
if curl -sf http://localhost:8002/health > /dev/null; then
    echo "✅ Dashboard is HEALTHY!"
else
    echo "⚠️  Health check failed, checking logs..."
    docker-compose logs --tail=30
    exit 1
fi

# Show status
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✨ DEPLOYMENT COMPLETE ✨"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Membership page:  https://dashboard.fullpotential.com/membership"
echo "📝 Signup:           https://dashboard.fullpotential.com/signup"
echo "🔑 Login:            https://dashboard.fullpotential.com/login"
echo "📊 Dashboard:        https://dashboard.fullpotential.com/dashboard"
echo ""
echo "💡 Test the complete flow:"
echo "   1. Visit /membership"
echo "   2. Click 'Get Started' on any tier"
echo "   3. Sign up with email/password"
echo "   4. Access member dashboard"
echo "   5. Try the AI tools!"
echo ""
echo "🎯 Next step: Add Stripe for payments"
echo ""

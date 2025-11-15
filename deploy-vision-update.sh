#!/bin/bash
# Deploy Vision/Mission/Values update to live server
# Run this ON THE SERVER (198.54.123.234)

set -e

echo "🚀 Deploying Vision/Mission/Values Update"
echo "========================================"
echo ""

# Navigate to dashboard directory
cd /opt/fpai/apps/dashboard/dashboard

# Backup current template
echo "📦 Creating backup..."
cp app/templates/paradise-progress.html app/templates/paradise-progress.html.backup.$(date +%Y%m%d_%H%M%S)

# Update the template (file will be transferred separately)
echo "⚠️  Please transfer the updated paradise-progress.html file to:"
echo "   /opt/fpai/apps/dashboard/dashboard/app/templates/paradise-progress.html"
echo ""
echo "Then restart the service:"
echo "   systemctl restart dashboard"
echo ""
echo "Or if using Docker:"
echo "   docker restart dashboard"
echo ""


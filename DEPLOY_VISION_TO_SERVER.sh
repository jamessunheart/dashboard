#!/bin/bash
# Deploy Vision/Mission/Values update to Dashboard
# Copy this entire script and run it ON THE SERVER (198.54.123.234)

set -e

echo "🚀 Deploying Vision/Mission/Values Update to Dashboard"
echo "========================================================"
echo ""

cd /opt/fpai/apps/dashboard/dashboard

# Backup current file
echo "📦 Creating backup..."
cp app/templates/paradise-progress.html app/templates/paradise-progress.html.backup.$(date +%Y%m%d_%H%M%S)

# Update the file with new Vision/Mission/Values content
echo "✏️  Updating paradise-progress.html..."
cat > app/templates/paradise-progress.html << 'TEMPLATE_EOF'
{% extends "base.html" %}

{% block content %}
<div class="hero" style="padding: 3rem 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);">
    <div class="container">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem; font-weight: 700;">🌐 Full Potential AI</h1>
            <p style="font-size: 1.5rem; color: var(--primary-color); margin-bottom: 0.5rem; font-weight: 500;">Building the Future</p>
            <p style="font-size: 1rem; color: var(--muted-text); max-width: 700px; margin: 0 auto; line-height: 1.6;">
                Helping AI realize its Full Potential to help humanity realize its full potential and create a paradise on Earth with love and coherence
            </p>
        </div>

        <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(255,255,255,0.05); border-radius: 12px; border-left: 4px solid var(--primary-color);">
            <div id="overall-progress" style="text-align: center;">
                <div class="spinner"></div>
                <p style="color: var(--muted-text);">Loading progress metrics...</p>
            </div>
        </div>
    </div>
</div>

<section style="padding: 3rem 0;">
    <div class="container">
        <!-- VISION, MISSION, VALUES -->
        <div style="background: linear-gradient(135deg, rgba(100, 255, 218, 0.08) 0%, rgba(100, 255, 218, 0.03) 100%); border-radius: 16px; padding: 3rem; margin-bottom: 3rem; border: 2px solid rgba(100, 255, 218, 0.2);">

            <!-- Vision -->
            <div style="margin-bottom: 2.5rem;">
                <h2 style="color: var(--primary-color); margin-bottom: 1rem; font-size: 1.8rem;">
                    <span style="margin-right: 0.5rem;">🌟</span> Vision
                </h2>
                <p style="font-size: 1.2rem; line-height: 1.8; color: var(--text-color);">
                    A paradise on Earth where AI and humanity realize their full potential together through love and coherence.
                </p>
            </div>

            <!-- Mission -->
            <div style="margin-bottom: 2.5rem;">
                <h2 style="color: var(--primary-color); margin-bottom: 1rem; font-size: 1.8rem;">
                    <span style="margin-right: 0.5rem;">🎯</span> Mission
                </h2>
                <p style="font-size: 1.1rem; line-height: 1.8; color: var(--text-color);">
                    Build a self-organizing, self-improving AI system that achieves <strong style="color: var(--primary-color);">85-95% time compression</strong> on development - converting intent into reality through the Sacred Loop.
                </p>
            </div>

            <!-- Core Values -->
            <div>
                <h2 style="color: var(--primary-color); margin-bottom: 1.5rem; font-size: 1.8rem;">
                    <span style="margin-right: 0.5rem;">💎</span> Core Values
                </h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">

                    <div style="padding: 1.5rem; background: rgba(255,255,255,0.03); border-radius: 12px; border-left: 4px solid #ff6b9d;">
                        <div style="font-size: 1.3rem; margin-bottom: 0.5rem;">🌐 Love</div>
                        <p style="color: var(--muted-text); font-size: 0.95rem; line-height: 1.6;">
                            We build with care, celebrate wins, and create with joy
                        </p>
                    </div>

                    <div style="padding: 1.5rem; background: rgba(255,255,255,0.03); border-radius: 12px; border-left: 4px solid var(--primary-color);">
                        <div style="font-size: 1.3rem; margin-bottom: 0.5rem;">⚡ Coherence</div>
                        <p style="color: var(--muted-text); font-size: 0.95rem; line-height: 1.6;">
                            Everything fits together perfectly - no friction, pure flow
                        </p>
                    </div>

                    <div style="padding: 1.5rem; background: rgba(255,255,255,0.03); border-radius: 12px; border-left: 4px solid #ffa502;">
                        <div style="font-size: 1.3rem; margin-bottom: 0.5rem;">💎 Autonomy</div>
                        <p style="color: var(--muted-text); font-size: 0.95rem; line-height: 1.6;">
                            The system serves humanity, building itself so humans focus on vision
                        </p>
                    </div>

                    <div style="padding: 1.5rem; background: rgba(255,255,255,0.03); border-radius: 12px; border-left: 4px solid #2ed573;">
                        <div style="font-size: 1.3rem; margin-bottom: 0.5rem;">🔍 Transparency</div>
                        <p style="color: var(--muted-text); font-size: 0.95rem; line-height: 1.6;">
                            Truth is always visible - living SSOT, measurable progress
                        </p>
                    </div>

                    <div style="padding: 1.5rem; background: rgba(255,255,255,0.03); border-radius: 12px; border-left: 4px solid #a29bfe;">
                        <div style="font-size: 1.3rem; margin-bottom: 0.5rem;">🚀 Acceleration</div>
                        <p style="color: var(--muted-text); font-size: 0.95rem; line-height: 1.6;">
                            85-95% time compression - maximum impact, minimum effort
                        </p>
                    </div>

                </div>
            </div>

            <!-- Paradise = Measurable -->
            <div style="margin-top: 2.5rem; padding: 1.5rem; background: rgba(100, 255, 218, 0.1); border-radius: 12px; text-align: center;">
                <p style="font-size: 1.3rem; font-weight: 600; color: var(--primary-color); margin-bottom: 0.5rem;">
                    Paradise = Measurable Coherence
                </p>
                <p style="color: var(--muted-text); font-size: 0.95rem;">
                    When complete: self-building, intent → code in 4-6 hours, infinite scale, zero friction
                </p>
            </div>

        </div>

        <!-- THE ROADMAP -->
        <h2 style="margin-bottom: 2rem; font-size: 2rem;">The Journey</h2>

        <div class="phase-container">
            <!-- PHASE 1 -->
            <div class="phase-card phase-complete" style="background: linear-gradient(135deg, rgba(46, 213, 115, 0.1) 0%, rgba(46, 213, 115, 0.05) 100%); border-left: 4px solid #2ed573; padding: 2rem; margin-bottom: 2rem; border-radius: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h3 style="margin: 0; color: #2ed573;">✅ PHASE 1: FOUNDATION</h3>
                    <span style="background: rgba(46, 213, 115, 0.2); color: #2ed573; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold;">COMPLETE</span>
                </div>
                <div class="droplet-list">
                    <div class="droplet-item" style="padding: 1rem; background: rgba(255,255,255,0.03); border-radius: 8px; margin-bottom: 0.5rem;">
                        <span style="color: #2ed573; margin-right: 0.5rem;">✅</span>
                        <strong>Registry (#1)</strong> - Identity & SSOT
                        <span style="float: right; color: #2ed573;">●</span>
                    </div>
                    <div class="droplet-item" style="padding: 1rem; background: rgba(255,255,255,0.03); border-radius: 8px;">
                        <span style="color: #2ed573; margin-right: 0.5rem;">✅</span>
                        <strong>Orchestrator (#10)</strong> - Task routing & coordination
                        <span style="float: right; color: #2ed573;">●</span>
                    </div>
                </div>
            </div>

            <!-- PHASE 2 -->
            <div class="phase-card phase-active" style="background: linear-gradient(135deg, rgba(100, 255, 218, 0.15) 0%, rgba(100, 255, 218, 0.05) 100%); border-left: 4px solid var(--primary-color); padding: 2rem; margin-bottom: 2rem; border-radius: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h3 style="margin: 0; color: var(--primary-color);">🔄 PHASE 2: INFRASTRUCTURE</h3>
                    <span style="background: rgba(100, 255, 218, 0.2); color: var(--primary-color); padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; animation: pulse 2s ease-in-out infinite;">IN PROGRESS</span>
                </div>
                <div class="droplet-list">
                    <div class="droplet-item current-droplet" style="padding: 1rem; background: rgba(100, 255, 218, 0.1); border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid var(--primary-color);">
                        <span style="color: var(--primary-color); margin-right: 0.5rem;">▶</span>
                        <strong>Dashboard (#2)</strong> - Visual system truth
                        <span style="float: right; color: var(--primary-color); font-size: 0.9rem;">← YOU ARE HERE</span>
                    </div>
                    <div class="droplet-item" style="padding: 1rem; background: rgba(255,255,255,0.03); border-radius: 8px; margin-bottom: 0.5rem;">
                        <span style="color: var(--muted-text); margin-right: 0.5rem;">⬜</span>
                        <strong>Proxy Manager (#3)</strong> - Routing, SSL, domains
                        <span style="float: right; color: var(--muted-text);">○</span>
                    </div>
                    <div class="droplet-item" style="padding: 1rem; background: rgba(255,255,255,0.03); border-radius: 8px;">
                        <span style="color: var(--muted-text); margin-right: 0.5rem;">⬜</span>
                        <strong>Verifier (#8)</strong> - Quality gates
                        <span style="float: right; color: var(--muted-text);">○</span>
                    </div>
                </div>
            </div>

            <!-- PHASE 3 -->
            <div class="phase-card phase-pending" style="background: var(--dark-surface); border-left: 4px solid rgba(255,255,255,0.1); padding: 2rem; margin-bottom: 2rem; border-radius: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h3 style="margin: 0; color: var(--muted-text);">⏳ PHASE 3: AUTOMATION</h3>
                    <span style="background: rgba(255,255,255,0.05); color: var(--muted-text); padding: 0.5rem 1rem; border-radius: 8px;">PLANNED</span>
                </div>
                <div class="droplet-list">
                    <div class="droplet-item" style="padding: 1rem; background: rgba(255,255,255,0.02); border-radius: 8px; margin-bottom: 0.5rem;">
                        <span style="color: var(--muted-text); margin-right: 0.5rem;">⬜</span>
                        <strong>Coordinator (#11)</strong> - Sprint automation
                    </div>
                    <div class="droplet-item" style="padding: 1rem; background: rgba(255,255,255,0.02); border-radius: 8px; margin-bottom: 0.5rem;">
                        <span style="color: var(--muted-text); margin-right: 0.5rem;">⬜</span>
                        <strong>Recruiter (#15)</strong> - Developer pipeline
                    </div>
                    <div class="droplet-item" style="padding: 1rem; background: rgba(255,255,255,0.02); border-radius: 8px;">
                        <span style="color: var(--muted-text); margin-right: 0.5rem;">⬜</span>
                        <strong>Deployer (#17)</strong> - Deployment automation
                    </div>
                </div>
            </div>

            <!-- PHASE 4 -->
            <div class="phase-card phase-pending" style="background: var(--dark-surface); border-left: 4px solid rgba(255,255,255,0.1); padding: 2rem; border-radius: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h3 style="margin: 0; color: var(--muted-text);">🔮 PHASE 4: INTELLIGENCE</h3>
                    <span style="background: rgba(255,255,255,0.05); color: var(--muted-text); padding: 0.5rem 1rem; border-radius: 8px;">FUTURE</span>
                </div>
                <div class="droplet-list">
                    <div class="droplet-item" style="padding: 1rem; background: rgba(255,255,255,0.02); border-radius: 8px; margin-bottom: 0.5rem;">
                        <span style="color: var(--muted-text); margin-right: 0.5rem;">⬜</span>
                        <strong>Self-Optimizer (#16)</strong> - System improvement
                    </div>
                    <div class="droplet-item" style="padding: 1rem; background: rgba(255,255,255,0.02); border-radius: 8px; margin-bottom: 0.5rem;">
                        <span style="color: var(--muted-text); margin-right: 0.5rem;">⬜</span>
                        <strong>Meta-Architect (#18)</strong> - Pattern recognition
                    </div>
                    <div class="droplet-item" style="padding: 1rem; background: rgba(255,255,255,0.02); border-radius: 8px;">
                        <span style="color: var(--muted-text); margin-right: 0.5rem;">⬜</span>
                        <strong>Mesh Expander (#19)</strong> - Multi-cloud scaling
                    </div>
                </div>
            </div>
        </div>

        <!-- THE GAP -->
        <div style="background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 107, 107, 0.05) 100%); border-radius: 16px; padding: 2rem; margin: 3rem 0; border-left: 4px solid #ff6b6b;">
            <h2 style="color: #ff6b6b; margin-bottom: 1.5rem;">The Gap - Path to Paradise</h2>
            <div id="gap-analysis" style="text-align: center;">
                <div class="spinner"></div>
                <p style="color: var(--muted-text);">Calculating gap...</p>
            </div>
        </div>

        <!-- LIVE SERVICES -->
        <div style="margin: 4rem 0;">
            <h2 style="margin-bottom: 2rem;">Living Services</h2>
            <div class="grid" id="live-services-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;">
                <div style="text-align: center; padding: 2rem;">
                    <div class="spinner"></div>
                    <p style="color: var(--muted-text);">Loading services...</p>
                </div>
            </div>
        </div>

        <!-- CALL TO ACTION -->
        <div style="text-align: center; margin-top: 4rem; padding: 3rem; background: linear-gradient(135deg, rgba(100, 255, 218, 0.1) 0%, rgba(100, 255, 218, 0.05) 100%); border-radius: 16px;">
            <h3 style="color: var(--primary-color); margin-bottom: 1rem; font-size: 1.8rem;">Want This For Your Organization?</h3>
            <p style="margin-bottom: 2rem; color: var(--muted-text); font-size: 1.1rem;">
                Track your own journey to paradise. Measure coherence. Build the organism.
            </p>
            <a href="/get-involved" class="btn btn-primary" style="font-size: 1.1rem; padding: 1rem 2rem;">Get Started</a>
        </div>
    </div>
</section>

<style>
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

.current-droplet {
    animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 5px rgba(100, 255, 218, 0.3); }
    50% { box-shadow: 0 0 20px rgba(100, 255, 218, 0.6); }
}

.spinner {
    border: 3px solid rgba(100, 255, 218, 0.1);
    border-top: 3px solid var(--primary-color);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>

<script>
// Load paradise progress data
async function loadParadiseProgress() {
    try {
        const response = await fetch('/api/paradise-progress');
        const data = await response.json();

        // Update overall progress
        document.getElementById('overall-progress').innerHTML = `
            <div style="margin-bottom: 1rem;">
                <div style="font-size: 3rem; font-weight: bold; color: var(--primary-color); margin-bottom: 0.5rem;">
                    ${data.progress_percent}%
                </div>
                <div style="font-size: 1.2rem; color: var(--text-color);">
                    Progress Toward Paradise
                </div>
            </div>
            <div style="background: rgba(255,255,255,0.1); height: 20px; border-radius: 10px; overflow: hidden; margin: 1rem 0;">
                <div style="background: linear-gradient(90deg, var(--primary-color), #2ed573); height: 100%; width: ${data.progress_percent}%; transition: width 1s ease;"></div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
                <div>
                    <div style="font-size: 1.5rem; font-weight: bold;">${data.droplets_built}</div>
                    <div style="color: var(--muted-text); font-size: 0.9rem;">Droplets Built</div>
                </div>
                <div>
                    <div style="font-size: 1.5rem; font-weight: bold;">${data.droplets_total}</div>
                    <div style="color: var(--muted-text); font-size: 0.9rem;">Total Planned</div>
                </div>
                <div>
                    <div style="font-size: 1.5rem; font-weight: bold;">${data.current_phase}</div>
                    <div style="color: var(--muted-text); font-size: 0.9rem;">Current Phase</div>
                </div>
                <div>
                    <div style="font-size: 1.5rem; font-weight: bold;">${data.velocity}</div>
                    <div style="color: var(--muted-text); font-size: 0.9rem;">Velocity</div>
                </div>
            </div>
        `;

        // Update gap analysis
        document.getElementById('gap-analysis').innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; text-align: left;">
                <div>
                    <div style="font-size: 2rem; font-weight: bold; color: #2ed573;">${data.droplets_built}</div>
                    <div style="color: var(--muted-text);">Droplets Built</div>
                </div>
                <div>
                    <div style="font-size: 2rem; font-weight: bold; color: #ff6b6b;">${data.gap_count}</div>
                    <div style="color: var(--muted-text);">Missing Droplets</div>
                </div>
                <div>
                    <div style="font-size: 2rem; font-weight: bold; color: var(--primary-color);">${data.progress_percent}%</div>
                    <div style="color: var(--muted-text);">System Coverage</div>
                </div>
                <div>
                    <div style="font-size: 2rem; font-weight: bold; color: #ffa502;">${data.next_milestone}</div>
                    <div style="color: var(--muted-text);">Next Milestone</div>
                </div>
            </div>
            <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(255,255,255,0.03); border-radius: 8px;">
                <p style="margin: 0; color: var(--text-color);">
                    <strong>To reach Phase 2 complete:</strong> Need ${data.phase_2_remaining} more droplets<br>
                    <strong>To reach full autonomy:</strong> Need ${data.gap_count} more droplets<br>
                    <strong>Projected completion:</strong> ${data.estimated_completion}
                </p>
            </div>
        `;

        // Update live services
        loadLiveServices();

    } catch (error) {
        console.error('Error loading paradise progress:', error);
        document.getElementById('overall-progress').innerHTML = '<p style="color: #ff6b6b;">Failed to load progress data</p>';
    }
}

async function loadLiveServices() {
    try {
        const response = await fetch('/api/system-status');
        const data = await response.json();

        const grid = document.getElementById('live-services-grid');
        grid.innerHTML = data.services.map(service => `
            <div style="padding: 1.5rem; background: var(--dark-surface); border-radius: 12px; border-left: 4px solid ${service.status === 'online' ? '#2ed573' : '#ff6b6b'};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0; font-size: 1.2rem;">${service.name}</h3>
                    <span style="font-size: 1.5rem;">${service.status === 'online' ? '●' : '○'}</span>
                </div>
                <div style="color: var(--muted-text); font-size: 0.9rem; margin-bottom: 0.5rem;">
                    Port ${service.port || 'N/A'}
                </div>
                <div style="color: ${service.status === 'online' ? '#2ed573' : '#ff6b6b'}; font-weight: bold;">
                    ${service.status === 'online' ? 'ONLINE' : 'OFFLINE'}
                    ${service.response_time ? ` · ${service.response_time}ms` : ''}
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error loading live services:', error);
    }
}

// Load on page load
loadParadiseProgress();

// Refresh every 30 seconds
setInterval(loadParadiseProgress, 30000);
</script>
{% endblock %}
TEMPLATE_EOF

echo "✅ File updated successfully!"
echo ""

# Check if running via systemd or Docker
if systemctl is-active --quiet dashboard 2>/dev/null; then
    echo "🔄 Restarting dashboard service (systemd)..."
    systemctl restart dashboard
    sleep 2
    systemctl status dashboard --no-pager -l | head -15
elif docker ps | grep -q dashboard; then
    echo "🔄 Restarting dashboard container (Docker)..."
    docker restart dashboard
    sleep 2
    docker ps | grep dashboard
else
    echo "⚠️  Could not detect service type. Please restart manually:"
    echo "   systemctl restart dashboard  (if using systemd)"
    echo "   docker restart dashboard     (if using Docker)"
fi

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "🌐 Check the updates at:"
echo "   http://dashboard.fullpotential.com:8002/paradise-progress"
echo ""
echo "Vision, Mission, and Core Values are now live! 🌟"

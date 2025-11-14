/**
 * Full Potential AI Dashboard - Main JavaScript
 * Handles live status updates and interactivity
 */

// Auto-update system status every 30 seconds
let statusUpdateInterval = null;

async function updateSystemStatus() {
    try {
        const response = await fetch('/api/system/status');
        const data = await response.json();

        // Update status widget if it exists
        const statusWidget = document.getElementById('system-status');
        if (statusWidget) {
            updateStatusWidget(data);
        }

        // Update live system page if it exists
        const liveSystem = document.getElementById('live-system-grid');
        if (liveSystem) {
            updateLiveSystem(data);
        }

    } catch (error) {
        console.error('Failed to fetch system status:', error);
        showStatusError();
    }
}

function updateStatusWidget(data) {
    const widget = document.getElementById('system-status');
    if (!widget) return;

    const healthClass = data.overall_health === 'healthy' ? 'status-online' :
                       data.overall_health === 'degraded' ? 'status-degraded' : 'status-offline';

    let html = `
        <h3>Live System Status</h3>
        <p class="${healthClass}" style="font-size: 1.2rem; font-weight: bold;">
            ${data.overall_health.toUpperCase()}
        </p>
    `;

    data.services.forEach(service => {
        const statusClass = service.status === 'online' ? 'status-online' :
                          service.status === 'degraded' ? 'status-degraded' : 'status-offline';
        const responseTime = service.response_time_ms ? `${service.response_time_ms}ms` : 'N/A';

        html += `
            <div class="status-item">
                <span>${service.name}</span>
                <span class="${statusClass}">
                    ● ${service.status.toUpperCase()} ${service.response_time_ms ? `(${responseTime})` : ''}
                </span>
            </div>
        `;
    });

    html += `
        <p style="text-align: center; margin-top: 1rem; color: var(--muted-text); font-size: 0.9rem;">
            ${data.droplet_count} droplets operational<br>
            <small>Updates every 30 seconds</small>
        </p>
    `;

    widget.innerHTML = html;
}

function updateLiveSystem(data) {
    const grid = document.getElementById('live-system-grid');
    if (!grid) return;

    // Update overall health
    const overallHealth = document.getElementById('overall-health');
    if (overallHealth) {
        const healthClass = data.overall_health === 'healthy' ? 'status-online' :
                           data.overall_health === 'degraded' ? 'status-degraded' : 'status-offline';
        overallHealth.innerHTML = `
            <h2>System Health: <span class="${healthClass}">${data.overall_health.toUpperCase()}</span></h2>
            <p>${data.droplet_count} droplets operational</p>
        `;
    }

    // Update service cards
    data.services.forEach(service => {
        const card = document.getElementById(`service-${service.name.toLowerCase()}`);
        if (card) {
            updateServiceCard(card, service);
        }
    });

    // Update last updated time
    const timestamp = document.getElementById('last-updated');
    if (timestamp) {
        timestamp.textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
    }
}

function updateServiceCard(card, service) {
    const statusClass = service.status === 'online' ? 'status-online' :
                       service.status === 'degraded' ? 'status-degraded' : 'status-offline';

    card.innerHTML = `
        <div class="droplet-header">
            <h3>${service.name}</h3>
            <span class="droplet-status ${service.status}"></span>
        </div>
        <p><strong>Status:</strong> <span class="${statusClass}">${service.status.toUpperCase()}</span></p>
        <p><strong>Response Time:</strong> ${service.response_time_ms || 'N/A'}ms</p>
        <p><strong>URL:</strong> <small>${service.url}</small></p>
        ${service.error ? `<p style="color: var(--danger-color);"><small>Error: ${service.error}</small></p>` : ''}
    `;
}

function showStatusError() {
    const widget = document.getElementById('system-status');
    if (widget) {
        widget.innerHTML = `
            <h3>Live System Status</h3>
            <p style="color: var(--danger-color);">Unable to fetch status</p>
            <p style="color: var(--muted-text); font-size: 0.9rem;">Retrying...</p>
        `;
    }
}

async function loadDroplets() {
    try {
        const response = await fetch('/api/droplets');
        const droplets = await response.json();

        const grid = document.getElementById('droplets-grid');
        if (!grid) return;

        grid.innerHTML = droplets.map(droplet => `
            <div class="droplet-card">
                <div class="droplet-header">
                    <h3>${droplet.name}</h3>
                    <span class="droplet-status ${droplet.status === 'active' ? 'online' : 'offline'}"></span>
                </div>
                <p><strong>ID:</strong> ${droplet.droplet_id}</p>
                <p><strong>Port:</strong> ${droplet.port || 'N/A'}</p>
                ${droplet.description ? `<p>${droplet.description}</p>` : ''}
                <div style="margin-top: 1rem;">
                    ${droplet.capabilities.map(cap =>
                        `<span style="display: inline-block; background: var(--dark-bg); padding: 0.25rem 0.5rem; border-radius: 4px; margin: 0.25rem; font-size: 0.85rem;">${cap}</span>`
                    ).join('')}
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Failed to load droplets:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Initial status update
    updateSystemStatus();

    // Load droplets if on live system page
    if (document.getElementById('droplets-grid')) {
        loadDroplets();
    }

    // Set up auto-update interval (30 seconds)
    statusUpdateInterval = setInterval(updateSystemStatus, 30000);
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (statusUpdateInterval) {
        clearInterval(statusUpdateInterval);
    }
});

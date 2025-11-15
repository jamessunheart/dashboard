# Droplet #2 - Dashboard

**Full Potential AI Dashboard** - Public marketing site and live system visualization

## Purpose

Dual-purpose web application that:
1. **Markets the vision** - Explains Full Potential AI to attract users, investors, and apprentices
2. **Shows the organism alive** - Real-time visualization of the FPAI system in action

## Features

- ✅ UDC-compliant (Universal Droplet Contract)
- ✅ Public marketing pages with vision and value proposition
- ✅ Live system status (auto-updates every 30s)
- ✅ Sacred Loop explanation
- ✅ Architecture documentation
- ✅ Get Involved / recruitment pages
- ✅ Real-time integration with Registry and Orchestrator
- ✅ Responsive mobile-first design
- ✅ Security headers and CORS configuration

## Tech Stack

- **Backend:** FastAPI (Python 3.11)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Deployment:** Docker
- **Testing:** pytest

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --port 8002
   ```

3. **Access the dashboard:**
   - Home: http://localhost:8002
   - Live System: http://localhost:8002/live-system
   - Sacred Loop: http://localhost:8002/sacred-loop

4. **Run tests:**
   ```bash
   pytest test/ -v
   ```

### Docker Deployment

1. **Build and run:**
   ```bash
   docker-compose up --build
   ```

2. **Access at:** http://localhost:8002

## UDC Endpoints

- `GET /health` - Service health status
- `GET /capabilities` - Droplet capabilities
- `GET /state` - Current state and uptime
- `GET /dependencies` - Service dependencies
- `POST /message` - Inter-droplet messaging

## API Endpoints

- `GET /api/system/status` - Aggregated system status
- `GET /api/droplets` - List of all droplets

## Web Pages

- `/` - Home page with vision and live status widget
- `/sacred-loop` - Sacred Loop explanation
- `/live-system` - Live system dashboard
- `/how-it-works` - Architecture and UDC documentation
- `/get-involved` - Recruitment and investment opportunities

## Configuration

Environment variables (see `.env.example`):
- `REGISTRY_URL` - Registry endpoint (default: http://198.54.123.234:8000)
- `ORCHESTRATOR_URL` - Orchestrator endpoint (default: http://198.54.123.234:8001)
- `PORT` - Service port (default: 8002)

## Deployment to Server

1. **Build Docker image:**
   ```bash
   docker build -t fpai-dashboard .
   ```

2. **Push to server and run:**
   ```bash
   # On server
   docker run -d \
     --name fpai-dashboard \
     -p 8002:8002 \
     -e REGISTRY_URL=http://198.54.123.234:8000 \
     -e ORCHESTRATOR_URL=http://198.54.123.234:8001 \
     --restart unless-stopped \
     fpai-dashboard
   ```

3. **Verify:**
   ```bash
   curl http://198.54.123.234:8002/health
   ```

## Architecture

The Dashboard follows the FPAI architecture:
- Registers with Registry on startup
- Sends heartbeat every 60 seconds
- Polls Registry/Orchestrator every 30 seconds for status
- Caches results to reduce load
- Gracefully degrades if services unavailable

## Live Integration

The Dashboard connects to:
- **Registry** (Port 8000) - For droplet directory and registration
- **Orchestrator** (Port 8001) - For system health metrics

Status updates happen automatically every 30 seconds via JavaScript polling of `/api/system/status`.

## Future Enhancements

- Contact form for investor/apprentice inquiries
- Email capture for newsletter
- Analytics dashboard
- Build progress visualization
- Integration with Coordinator for live sprint tracking
- Admin panel for content management

## Success Metrics

- ✅ All UDC endpoints implemented
- ✅ Live system status showing Registry + Orchestrator
- ✅ Responsive design works on mobile
- ✅ Page load time <2s
- ✅ API response time <200ms

---

**Version:** 1.0.0
**Status:** MVP Complete
**Deployment:** http://198.54.123.234:8002 (soon: fullpotential.ai)

🌐⚡💎
# Automated Deployments Active

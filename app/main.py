"""
Dashboard Main Application
Droplet #2 - Public marketing site and system visualization
Follows FPAI architecture and UDC compliance
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import asyncio
import logging
from pathlib import Path

from app.config import settings
from app.routers import udc, api, auth, tools
from app.routers.auth import get_current_user
from app.services.registry_client import registry_client

# Configure logging (follows CODE_STANDARDS.md - structured logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Background task for heartbeat
heartbeat_task = None


async def send_heartbeat_loop():
    """Background task to send heartbeat to Registry every 60s"""
    while True:
        try:
            await asyncio.sleep(settings.heartbeat_interval)
            success = await registry_client.send_heartbeat()
            if success:
                logger.debug("Heartbeat sent successfully")
            else:
                logger.warning("Heartbeat failed")
        except Exception as e:
            logger.error(f"Heartbeat loop error: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management - startup and shutdown"""
    global heartbeat_task

    # Startup
    logger.info(f"Starting {settings.droplet_name} v{settings.version}")

    # Register with Registry
    logger.info("Registering with Registry...")
    registration_success = await registry_client.register()
    if registration_success:
        logger.info("✅ Successfully registered with Registry")
    else:
        logger.warning("⚠️ Registration failed - will retry on heartbeat")

    # Start heartbeat background task
    heartbeat_task = asyncio.create_task(send_heartbeat_loop())
    logger.info("Started heartbeat task")

    yield

    # Shutdown
    logger.info("Shutting down Dashboard...")
    if heartbeat_task:
        heartbeat_task.cancel()
        try:
            await heartbeat_task
        except asyncio.CancelledError:
            pass
    logger.info("Shutdown complete")


# Initialize FastAPI app
app = FastAPI(
    title="Full Potential AI - Dashboard",
    description="Public marketing site and system visualization",
    version=settings.version,
    lifespan=lifespan
)

# CORS middleware (allow all origins for public site)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Mount static files and templates
static_path = Path(__file__).parent / "static"
templates_path = Path(__file__).parent / "templates"

app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
templates = Jinja2Templates(directory=str(templates_path))

# Include routers
app.include_router(udc.router, tags=["UDC"])
app.include_router(api.router, tags=["API"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(tools.router, tags=["Tools"])


# Web Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - Vision and marketing"""
    return templates.TemplateResponse("home.html", {
        "request": request,
        "title": "Full Potential AI",
        "version": settings.version
    })


@app.get("/sacred-loop", response_class=HTMLResponse)
async def sacred_loop(request: Request):
    """Sacred Loop explanation page"""
    return templates.TemplateResponse("sacred-loop.html", {
        "request": request,
        "title": "The Sacred Loop - Full Potential AI"
    })


@app.get("/live-system", response_class=HTMLResponse)
async def live_system(request: Request):
    """Live system status page"""
    return templates.TemplateResponse("live-system.html", {
        "request": request,
        "title": "Live System - Full Potential AI"
    })


@app.get("/how-it-works", response_class=HTMLResponse)
async def how_it_works(request: Request):
    """Architecture and how it works page"""
    return templates.TemplateResponse("how-it-works.html", {
        "request": request,
        "title": "How It Works - Full Potential AI"
    })


@app.get("/get-involved", response_class=HTMLResponse)
async def get_involved(request: Request):
    """Get involved page - recruitment and investment"""
    return templates.TemplateResponse("get-involved.html", {
        "request": request,
        "title": "Get Involved - Full Potential AI"
    })


@app.get("/paradise-progress", response_class=HTMLResponse)
async def paradise_progress(request: Request):
    """Paradise Progress - Journey to coherence dashboard"""
    return templates.TemplateResponse("paradise-progress.html", {
        "request": request,
        "title": "Paradise Progress - Full Potential AI"
    })


@app.get("/membership", response_class=HTMLResponse)
async def membership(request: Request):
    """Membership landing page - Full Potential personal growth subscription"""
    return templates.TemplateResponse("membership.html", {
        "request": request,
        "title": "Full Potential Membership - Unlock Your Potential with AI"
    })


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Member dashboard - requires authentication"""
    user = get_current_user(request)

    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "Dashboard - Full Potential",
        "user": user
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True,
        log_level="info"
    )

"""
AI Tools Router
Member-only tools for personal growth
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.routers.auth import get_current_user

router = APIRouter(prefix="/tools")
templates_path = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


def require_auth(request: Request):
    """Middleware to require authentication"""
    user = get_current_user(request)
    if not user:
        return None
    return user


@router.get("/goals", response_class=HTMLResponse)
async def goals_tool(request: Request):
    """Goal Setting Assistant Tool"""
    user = require_auth(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("tool-goals.html", {
        "request": request,
        "title": "Goal Setting Assistant - Full Potential",
        "user": user
    })


@router.get("/reflection", response_class=HTMLResponse)
async def reflection_tool(request: Request):
    """Daily Reflection Prompter Tool"""
    user = require_auth(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("tool-reflection.html", {
        "request": request,
        "title": "Daily Reflection - Full Potential",
        "user": user
    })


@router.get("/strengths", response_class=HTMLResponse)
async def strengths_tool(request: Request):
    """Strengths Finder Tool"""
    user = require_auth(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("tool-strengths.html", {
        "request": request,
        "title": "Strengths Finder - Full Potential",
        "user": user
    })

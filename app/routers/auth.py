"""
Authentication Router
Handles signup, login, logout for Full Potential Membership
"""
from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import re

from app.database import (
    create_user,
    get_user_by_email,
    verify_password,
    create_session,
    delete_session,
    verify_session
)

router = APIRouter()
templates_path = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


def is_valid_email(email: str) -> bool:
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request, tier: str = "builder"):
    """Signup page"""
    return templates.TemplateResponse("signup.html", {
        "request": request,
        "title": "Sign Up - Full Potential",
        "tier": tier,
        "error": None
    })


@router.post("/signup")
async def signup_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    tier: str = Form(default="seeker")
):
    """Handle signup form submission"""

    # Validation
    errors = []

    if not is_valid_email(email):
        errors.append("Please enter a valid email address")

    if len(password) < 8:
        errors.append("Password must be at least 8 characters")

    if not full_name.strip():
        errors.append("Please enter your full name")

    if tier not in ['seeker', 'builder', 'master']:
        errors.append("Invalid membership tier")

    if errors:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "title": "Sign Up - Full Potential",
            "tier": tier,
            "error": " | ".join(errors),
            "email": email,
            "full_name": full_name
        })

    # Create user
    user_id = create_user(email.lower().strip(), password, full_name.strip(), tier)

    if user_id is None:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "title": "Sign Up - Full Potential",
            "tier": tier,
            "error": "An account with this email already exists. Try logging in instead.",
            "email": email,
            "full_name": full_name
        })

    # Create session
    token = create_session(user_id)

    # Redirect to dashboard with session cookie
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=86400,  # 24 hours
        samesite="lax"
    )

    return response


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "title": "Login - Full Potential",
        "error": None
    })


@router.post("/login")
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    """Handle login form submission"""

    # Get user
    user = get_user_by_email(email.lower().strip())

    if not user or not verify_password(password, user['password_hash']):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "title": "Login - Full Potential",
            "error": "Invalid email or password",
            "email": email
        })

    if not user['is_active']:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "title": "Login - Full Potential",
            "error": "Your account has been deactivated. Please contact support.",
            "email": email
        })

    # Create session
    token = create_session(user['id'])

    # Redirect to dashboard
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=86400,
        samesite="lax"
    )

    return response


@router.get("/logout")
async def logout(request: Request):
    """Logout user"""
    token = request.cookies.get("session_token")

    if token:
        delete_session(token)

    response = RedirectResponse(url="/membership", status_code=303)
    response.delete_cookie("session_token")

    return response


def get_current_user(request: Request):
    """Get current logged-in user from session cookie"""
    token = request.cookies.get("session_token")

    if not token:
        return None

    return verify_session(token)

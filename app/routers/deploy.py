"""
Deploy Webhook - No more SSH or line wrapping!
Just visit /deploy?secret=YOUR_SECRET to deploy
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import subprocess
import os

router = APIRouter()

# Set this in environment or use default
DEPLOY_SECRET = os.getenv("DEPLOY_SECRET", "fpai-deploy-2025")

@router.post("/deploy")
@router.get("/deploy")
async def deploy_webhook(secret: str = Query(..., description="Deploy secret key")):
    """
    Webhook to deploy latest code
    Usage: curl http://your-server:8002/deploy?secret=YOUR_SECRET
    """

    # Verify secret
    if secret != DEPLOY_SECRET:
        raise HTTPException(status_code=403, detail="Invalid deploy secret")

    try:
        # Pull latest code
        pull_result = subprocess.run(
            ["git", "pull"],
            cwd="/app",
            capture_output=True,
            text=True,
            timeout=30
        )

        # Check if there were updates
        pull_output = pull_result.stdout + pull_result.stderr
        has_updates = "Already up to date" not in pull_output

        if has_updates:
            # Restart container from inside
            # Note: This will cause a brief interruption
            subprocess.Popen(
                ["sh", "-c", "sleep 2 && kill -HUP 1"],
                cwd="/app"
            )

            return JSONResponse({
                "status": "success",
                "message": "Deployed! Container restarting...",
                "updates": True,
                "output": pull_output[:500]  # First 500 chars
            })
        else:
            return JSONResponse({
                "status": "success",
                "message": "Already up to date - no deployment needed",
                "updates": False,
                "output": pull_output
            })

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Deploy timeout - git pull took too long")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deploy failed: {str(e)}")


@router.get("/deploy-status")
async def deploy_status():
    """Check current deployment status"""
    try:
        # Get current git commit
        commit_result = subprocess.run(
            ["git", "log", "-1", "--oneline"],
            cwd="/app",
            capture_output=True,
            text=True,
            timeout=5
        )

        # Get current branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd="/app",
            capture_output=True,
            text=True,
            timeout=5
        )

        return {
            "current_commit": commit_result.stdout.strip(),
            "current_branch": branch_result.stdout.strip(),
            "deploy_url": f"/deploy?secret={DEPLOY_SECRET}",
            "instructions": "GET or POST to /deploy?secret=YOUR_SECRET to deploy"
        }

    except Exception as e:
        return {"error": str(e)}

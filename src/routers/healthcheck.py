from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"]
)

@router.get("/")
async def healthcheck():
    try:
        return {
            "status": "Service is running",
            "datetime": datetime.now().isoformat()
        }

    except HTTPException as e:
        return {"error": str(e.detail)}

    except Exception as e:
        return {"error": "An unexpected error occurred"}

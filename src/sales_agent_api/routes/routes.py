from fastapi import APIRouter, HTTPException
from src.sales_agent_api.controller.controller import (
    sales_info_search_controller,
    get_thread_controller,
    generate_thread_id_controller,
)
from src.sales_agent_api.models.models import SalesInfoSearchRequest
from src.app import app

router = APIRouter()

@router.get("/", tags=["Health"])
async def root():
    return {
        "status": "Sales Info Search Agent API is running",
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }

@router.get("/health", tags=["Health"])
async def health_check():
    status = "healthy" if getattr(app, "agent", None) is not None else "unhealthy"
    return {
        "status": status,
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }

@router.post("/search-sales-info", tags=["SalesInfo"])
async def sales_info_search_endpoint(request: SalesInfoSearchRequest):
    if getattr(app, "agent", None) is None:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    return await sales_info_search_controller(app.agent, request)

@router.get("/threads/{thread_id}", tags=["Thread"])
async def get_thread(thread_id: str):
    return await get_thread_controller(thread_id)

@router.get("/threads", tags=["Thread"])
async def generate_thread():
    return await generate_thread_id_controller()
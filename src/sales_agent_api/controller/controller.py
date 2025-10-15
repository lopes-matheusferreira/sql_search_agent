from src.sales_agent_api.service.service import (
    run_sales_info_search_service,
    get_thread_service,
    generate_thread_id_service,
)
from typing import Any

async def sales_info_search_controller(agent, request: Any):
    return await run_sales_info_search_service(agent, request.message, request.thread_id)

async def get_thread_controller(thread_id: str):
    return await get_thread_service(thread_id)

async def generate_thread_id_controller():
    return await generate_thread_id_service()
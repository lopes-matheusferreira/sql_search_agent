"""
FastAPI application with RedisSaver checkpointer.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← ADICIONE ISSO
from pathlib import Path
import sys

project_root = Path(__file__).parent
sys.path.append(str(project_root))

from sales_info_agent.main import create_sales_info_search_agent
from src.redis.config import redis_client

app = FastAPI(
    title="Sales Info Search Agent API",
    description="API for interacting with the sales information search agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print("Initializing Sales Info Search Agent with RedisSaver...")

    try:
        redis_client.ping()
        print("Connected to Redis successfully!")

        app.agent = create_sales_info_search_agent()
        print("Agent initialized successfully with persistent storage!")

    except Exception as e:
        print(f"Error during startup: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down Sales Info Search Agent...")


from src.sales_agent_api.routes.routes import router

app.include_router(router)
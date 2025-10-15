"""
Redis configuration for LangGraph checkpointer.
Centralizes Redis connection for both checkpointer and custom operations.
"""

import os
from redis import Redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def get_redis_connection():
    """
    Get Redis connection for LangGraph checkpointer.
    """
    return Redis.from_url(REDIS_URL, decode_responses=False)

redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
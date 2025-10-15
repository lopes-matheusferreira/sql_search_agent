import json
from src.redis.config import redis_client

async def save_thread_interaction(thread_id: str, data: dict):
    """Salvar interação no Redis"""
    redis_client.set(thread_id, json.dumps(data))

async def get_thread_interactions(thread_id: str):
    """Buscar interação no Redis"""
    data = redis_client.get(thread_id)
    if data:
        return json.loads(data)
    return None

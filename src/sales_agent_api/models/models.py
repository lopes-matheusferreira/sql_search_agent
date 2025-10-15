from pydantic import BaseModel
from typing import Optional

class SalesInfoSearchRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None
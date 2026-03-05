from pydantic import BaseModel
from typing import Optional


class CurrentUser(BaseModel):
    user_id: str
    email: Optional[str] = None
    role: str

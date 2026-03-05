from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class PersonaBase(BaseModel):
    name: str
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    system_prompt: str
    is_active: bool = True


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    system_prompt: Optional[str] = None
    is_active: Optional[bool] = None


class PersonaResponse(PersonaBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SelectPersonaRequest(BaseModel):
    persona_id: int

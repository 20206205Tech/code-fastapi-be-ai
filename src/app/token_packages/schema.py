from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TokenPackageBase(BaseModel):
    name: str = Field(...)
    token: int = Field(..., gt=0)
    price: Decimal = Field(...,  gt=0)
    is_active: Optional[bool] = Field(default=True)


class TokenPackageCreate(TokenPackageBase):
    pass


class TokenPackageUpdate(BaseModel):
    name: Optional[str] = None
    token: Optional[int] = Field(None, gt=0)
    price: Optional[Decimal] = Field(None, gt=0)
    is_active: Optional[bool] = None


class TokenPackageResponse(TokenPackageBase):
    id: int
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

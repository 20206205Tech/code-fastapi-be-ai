from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TokenPackageBase(BaseModel):
    name: str = Field(..., description="Tên gói token")
    token: int = Field(..., description="Số lượng token")
    price: Decimal = Field(..., description="Giá tiền")
    is_active: Optional[bool] = Field(
        default=True, description="Trạng thái hiển thị gói")


class TokenPackageCreate(TokenPackageBase):
    pass


class TokenPackageUpdate(BaseModel):
    name: Optional[str] = None
    token: Optional[int] = None
    price: Optional[Decimal] = None
    is_active: Optional[bool] = None


class TokenPackageResponse(TokenPackageBase):
    id: int
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

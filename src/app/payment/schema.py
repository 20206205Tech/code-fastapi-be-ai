from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TransactionHistoryResponse(BaseModel):
    id: int
    package_id: int
    amount_paid: Decimal
    tokens_added: int
    payment_method: Optional[str]
    transaction_ref: Optional[str]
    status: str
    created_at: datetime

    # Thêm thông tin từ gói nếu cần
    # package_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

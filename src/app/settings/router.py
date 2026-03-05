from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.auth.dependencies import get_current_user_id
from app.common.response.base_response import BaseResponse
from .schema import SettingItem, UpsertSettingsRequest
from .service import get_user_settings, upsert_user_settings

router = APIRouter(prefix="/settings", tags=["User Settings"])


@router.get("/", response_model=BaseResponse[List[SettingItem]])
def get_settings(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    data = get_user_settings(db, user_id)
    return BaseResponse(
        success=True,
        message="Lấy cài đặt thành công",
        data=data
    )


@router.post("/", response_model=BaseResponse)
def upsert_settings(
    request: UpsertSettingsRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    upsert_user_settings(db, user_id, request)
    return BaseResponse(
        success=True,
        message="Cập nhật cài đặt thành công"
    )

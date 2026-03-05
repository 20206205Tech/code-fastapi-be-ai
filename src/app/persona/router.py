import uuid
from app.common.supabase_client import supabase
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi import APIRouter, Depends
import settings
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.auth.dependencies import get_current_user_id, require_admin
from app.auth.schemas import CurrentUser
from app.common.response.base_response import BaseResponse
from . import service, schema


router = APIRouter(prefix="/personas", tags=["Personas"])


@router.post("", response_model=BaseResponse[schema.PersonaResponse])
def create_persona(
    request: schema.PersonaCreate,
    admin: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    data = service.create_persona(db, request)
    return BaseResponse(success=True, message="Tạo nhân vật thành công", data=data)


@router.put("/{persona_id}", response_model=BaseResponse[schema.PersonaResponse])
def update_persona(
    persona_id: int,
    request: schema.PersonaUpdate,
    admin: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    data = service.update_persona(db, persona_id, request)
    return BaseResponse(success=True, message="Cập nhật thành công", data=data)


@router.delete("/{persona_id}")
def delete_persona(
    persona_id: int,
    admin: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    service.delete_persona(db, persona_id)
    return BaseResponse(success=True, message="Xóa nhân vật thành công")

# --- USER ENDPOINTS ---


@router.get("", response_model=BaseResponse[List[schema.PersonaResponse]])
def get_all_personas(db: Session = Depends(get_db)):
    data = service.get_personas(db)
    return BaseResponse(success=True, message="Thành công", data=data)


@router.post("/select", response_model=BaseResponse)
def select_persona(
    request: schema.SelectPersonaRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service.select_persona_for_user(db, user_id, request.persona_id)
    return BaseResponse(success=True, message="Đã lựa chọn nhân vật để trò chuyện")


@router.post("/upload-avatar", response_model=BaseResponse[str])
async def upload_persona_avatar(
    file: UploadFile = File(...),
    admin: CurrentUser = Depends(require_admin)
):
    # Gọi logic từ service
    public_url = await service.upload_persona_avatar(file)

    return BaseResponse(
        success=True,
        message="Tải ảnh nhân vật thành công",
        data=public_url
    )

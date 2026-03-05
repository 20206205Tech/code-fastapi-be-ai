from fastapi import UploadFile, HTTPException
from app.common.supabase_client import supabase
import settings
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Persona, UserSettings
from .schema import PersonaCreate, PersonaUpdate


def get_personas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Persona).filter(Persona.is_active == True).offset(skip).limit(limit).all()


def get_persona_by_id(db: Session, persona_id: int):
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhân vật")
    return persona


def create_persona(db: Session, obj_in: PersonaCreate):
    db_obj = Persona(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_persona(db: Session, persona_id: int, obj_in: PersonaUpdate):
    db_obj = get_persona_by_id(db, persona_id)
    update_data = obj_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_persona(db: Session, persona_id: int):
    db_obj = get_persona_by_id(db, persona_id)
    db.delete(db_obj)
    db.commit()
    return True


def select_persona_for_user(db: Session, user_id: str, persona_id: int):
    # Kiểm tra persona có tồn tại không
    persona = get_persona_by_id(db, persona_id)

    # Lưu vào bảng UserSettings với key là 'selected_persona_id'
    setting = db.query(UserSettings).filter(
        UserSettings.user_id == user_id,
        UserSettings.key == "selected_persona_id"
    ).first()

    if setting:
        setting.value = str(persona_id)
    else:
        setting = UserSettings(
            user_id=user_id,
            key="selected_persona_id",
            value=str(persona_id)
        )
        db.add(setting)

    db.commit()
    return persona


async def upload_persona_avatar(file: UploadFile) -> str:
    # 1. Kiểm tra định dạng file
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Định dạng ảnh không hợp lệ: {file_ext}. Chỉ chấp nhận: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
        )

    # 2. Chuẩn bị thông tin upload
    bucket_id = settings.PERSONA_AVATARS_BUCKET
    file_name = f"avatar_{uuid.uuid4()}.{file_ext}"

    try:
        # Đọc nội dung file
        file_content = await file.read()

        # 3. Upload lên Supabase Storage
        supabase.storage.from_(bucket_id).upload(
            path=file_name,
            file=file_content,
            file_options={"content-type": file.content_type}
        )

        # 4. Lấy URL công khai
        public_url = supabase.storage.from_(
            bucket_id).get_public_url(file_name)

        return public_url

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Lỗi khi tải ảnh lên: {str(e)}")

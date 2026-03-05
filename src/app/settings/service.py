from sqlalchemy.orm import Session
from models import UserSettings
from .schema import UpsertSettingsRequest


def get_user_settings(db: Session, user_id: str):
    return db.query(UserSettings).filter(UserSettings.user_id == user_id).all()


def upsert_user_settings(db: Session, user_id: str, request: UpsertSettingsRequest):
    existing_settings = db.query(UserSettings).filter(
        UserSettings.user_id == user_id).all()

    existing_map = {setting.key: setting for setting in existing_settings}

    for item in request.settings:
        if item.key in existing_map:
            existing_map[item.key].value = item.value
        else:
            new_setting = UserSettings(
                user_id=user_id, key=item.key, value=item.value)
            db.add(new_setting)

    db.commit()
    return True

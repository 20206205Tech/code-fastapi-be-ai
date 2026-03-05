from pydantic import BaseModel
from typing import List


class SettingItem(BaseModel):
    key: str
    value: str


class UpsertSettingsRequest(BaseModel):
    settings: List[SettingItem]

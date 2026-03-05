from fastapi import APIRouter


from app.settings.router import router as settings_router


index_router = APIRouter()


index_router.include_router(settings_router)

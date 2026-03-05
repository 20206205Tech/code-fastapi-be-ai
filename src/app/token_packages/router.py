from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from app.auth.dependencies import require_admin
from app.auth.schemas import CurrentUser
from app.common.response.base_response import BaseResponse

from .schema import TokenPackageCreate, TokenPackageUpdate, TokenPackageResponse
from . import service

router = APIRouter(prefix="/token-packages", tags=["Token Packages"])


@router.get("", response_model=BaseResponse[List[TokenPackageResponse]])
def get_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = service.get_all_packages(db, skip, limit)
    return BaseResponse(
        success=True,
        message="Lấy danh sách gói token thành công",
        data=data
    )


@router.get("/{package_id}", response_model=BaseResponse[TokenPackageResponse])
def get_package(package_id: int, db: Session = Depends(get_db)):
    data = service.get_package_by_id(db, package_id)
    return BaseResponse(
        success=True,
        message="Lấy thông tin gói token thành công",
        data=data
    )


@router.post("", response_model=BaseResponse[TokenPackageResponse])
def create_package(
    request: TokenPackageCreate,
    admin: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    data = service.create_package(db, request)
    return BaseResponse(
        success=True,
        message="Tạo gói token thành công",
        data=data
    )


@router.put("/{package_id}", response_model=BaseResponse[TokenPackageResponse])
def update_package(
    package_id: int,
    request: TokenPackageUpdate,
    admin: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    data = service.update_package(db, package_id, request)
    return BaseResponse(
        success=True,
        message="Cập nhật gói token thành công",
        data=data
    )


@router.delete("/{package_id}", response_model=BaseResponse)
def delete_package(
    package_id: int,
    admin: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    service.delete_package(db, package_id)
    return BaseResponse(
        success=True,
        message="Xóa gói token thành công"
    )

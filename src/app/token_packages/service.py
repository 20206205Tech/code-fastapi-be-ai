from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import TokenPackages
from .schema import TokenPackageCreate, TokenPackageUpdate


def get_all_packages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TokenPackages).offset(skip).limit(limit).all()


def get_package_by_id(db: Session, package_id: int):
    package = db.query(TokenPackages).filter(
        TokenPackages.id == package_id).first()
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy gói token"
        )
    return package


def create_package(db: Session, request: TokenPackageCreate):
    new_package = TokenPackages(**request.model_dump())
    db.add(new_package)
    db.commit()
    db.refresh(new_package)
    return new_package


def update_package(db: Session, package_id: int, request: TokenPackageUpdate):
    db_package = get_package_by_id(db, package_id)

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_package, key, value)

    db.commit()
    db.refresh(db_package)
    return db_package


def delete_package(db: Session, package_id: int):
    db_package = get_package_by_id(db, package_id)
    db.delete(db_package)
    db.commit()
    return True

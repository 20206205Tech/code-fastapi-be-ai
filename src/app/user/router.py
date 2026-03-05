# import settings
# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy.orm import Session
# from database import get_db
# from models import User
# from app.user.schema import UserCreate, UserUpdate
# from fastapi import APIRouter


# router = FastAPI()
# router = APIRouter(prefix="/users", tags=["users"])


# @router.get("/users/")
# def get_all_users(db: Session = Depends(get_db)):
#     return db.query(User).all()


# @router.get("/users/{user_id}")
# def get_user_by_email(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if user:
#         return user
#     raise HTTPException(status_code=404, detail="User not found")


# @router.post("/users/")
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = User(name=user.name, email=user.email, password=user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# @router.put("/users/{user_id}")
# def update_user_by_email(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db_user.name = user.name
#     db_user.email = user.email
#     db.commit()
#     return {"message": "User updated successfully"}


# @router.delete("/users/{user_id}")
# def delete_user_by_email(user_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(db_user)
#     db.commit()
#     return {"message": "User deleted successfully"}

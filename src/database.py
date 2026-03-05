from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import settings


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Thêm dòng này để kiểm tra connection trước khi dùng
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
import datetime
from sqlalchemy import String, Integer, Float, DateTime, JSON, PrimaryKeyConstraint, Index, text, Identity, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RequestLog(Base):
    __tablename__ = "request_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    request_id: Mapped[Optional[str]] = mapped_column(
        String(255), index=True, nullable=True)  # Lấy từ Kong
    method: Mapped[str] = mapped_column(String(10))
    url: Mapped[str] = mapped_column(String(255))
    client_ip: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status_code: Mapped[int] = mapped_column(Integer)

    # Cột lưu Body Request & Response
    request_payload: Mapped[Optional[dict]
                            ] = mapped_column(JSON, nullable=True)
    response_payload: Mapped[Optional[dict]
                             ] = mapped_column(JSON, nullable=True)

    process_time: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())


# class User(Base):
#     __tablename__ = "users"
#     id: int = Column(Integer, primary_key=True, index=True)
#     name: str = Column(String(50), index=True)
#     email: str = Column(String(50), unique=True, index=True)
#     password: str = Column(String(50))


class UserSettings(Base):
    __tablename__ = 'user_settings'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_settings_pkey'),
        Index('unique_user_key', 'user_id', 'key', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, Identity(
        start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)

    user_id: Mapped[str] = mapped_column(String(36), nullable=False)

    key: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()'))

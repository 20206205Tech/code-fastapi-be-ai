from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Identity, Integer, Numeric, PrimaryKeyConstraint, String, text
import decimal
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
import datetime
from sqlalchemy import String, Integer, Float, DateTime, JSON, PrimaryKeyConstraint, Index, text, Identity, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Enum, ForeignKeyConstraint, Identity, Integer, Numeric, PrimaryKeyConstraint, String, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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


class TokenPackages(Base):
    __tablename__ = 'token_packages'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='token_packages_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(
        start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text('true'), comment='Trạng thái hiển thị gói')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()'))

    transactions: Mapped[list['Transactions']] = relationship(
        'Transactions', back_populates='package')


class Tokens(Base):
    __tablename__ = 'tokens'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tokens_pkey'),
        UniqueConstraint('user_id', name='tokens_user_id_key')
    )

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36), nullable=False)
    balance: Mapped[Optional[int]] = mapped_column(
        Integer, server_default=text('0'))


class Transactions(Base):
    __tablename__ = 'transactions'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['token_packages.id'],
                             deferrable=True, name='transactions_package_id_fkey'),
        PrimaryKeyConstraint('id', name='transactions_pkey'),
        UniqueConstraint('transaction_ref',
                         name='transactions_transaction_ref_key')
    )

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36), nullable=False)
    package_id: Mapped[int] = mapped_column(Integer, nullable=False)
    amount_paid: Mapped[decimal.Decimal] = mapped_column(
        Numeric, nullable=False)
    tokens_added: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_method: Mapped[Optional[str]] = mapped_column(
        String, default="VNPAY")
    transaction_ref: Mapped[Optional[str]] = mapped_column(
        String)
    status: Mapped[Optional[str]] = mapped_column(Enum(
        'pending', 'success', 'failed', name='transaction_status'), server_default=text("'pending'::transaction_status"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()'), onupdate=text('now()'))

    vnp_transaction_no: Mapped[Optional[str]
                               ] = mapped_column(String(50), nullable=True)
    vnp_response_code: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True)
    bank_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    pay_date: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    package: Mapped['TokenPackages'] = relationship(
        'TokenPackages', back_populates='transactions')

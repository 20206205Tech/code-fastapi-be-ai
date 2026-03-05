from .schema import TransactionHistoryResponse  # Import schema đã tạo ở bước 1
from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from app.auth.dependencies import get_current_user_id
from app.common.response.base_response import BaseResponse
from . import service
from fastapi.responses import PlainTextResponse


router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post("/buy-package/{package_id}")
def buy_token_package(
    package_id: int,
    request: Request,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    client_ip = request.client.host
    payment_url = service.create_payment_url(
        db, user_id, package_id, client_ip)

    # return BaseResponse(
    #     success=True,
    #     message="Tạo link thanh toán thành công",
    #     data={"payment_url": payment_url}
    # )
    return PlainTextResponse(payment_url)


@router.get("/vnpay-return", response_model=BaseResponse, include_in_schema=False)
def vnpay_return(request: Request, db: Session = Depends(get_db)):
    query_params = dict(request.query_params)
    result = service.process_vnpay_return(db, query_params)

    return BaseResponse(
        success=result["success"],
        message=result["message"],
        data=result.get("tokens_added")
    )


@router.get("/history", response_model=BaseResponse[List[TransactionHistoryResponse]])
def get_payment_history(
    skip: int = 0,
    limit: int = 20,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    history = service.get_user_payment_history(db, user_id, skip, limit)

    return BaseResponse(
        success=True,
        message="Lấy lịch sử thanh toán thành công",
        data=history
    )

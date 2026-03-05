from models import Transactions
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
import datetime
import settings
from models import TokenPackages, Transactions, Tokens
from .vnpay_core import Vnpay  # Đặt file class Vnpay vào cùng thư mục

vnpay = Vnpay(
    tmn_code=settings.VNPAY_TMN_CODE,
    secret_key=settings.VNPAY_HASH_SECRET_KEY,
    return_url=settings.VNPAY_RETURN_URL,
    vnpay_payment_url=settings.VNPAY_PAYMENT_URL,
    api_url=settings.VNPAY_API_URL
)


def create_payment_url(db: Session, user_id: str, package_id: int, client_ip: str) -> str:
    # 1. Kiểm tra gói token
    package = db.query(TokenPackages).filter(
        TokenPackages.id == package_id, TokenPackages.is_active == True).first()
    if not package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Gói token không tồn tại hoặc đã vô hiệu hóa")

    # 2. Tạo mã giao dịch (TxnRef)
    txn_ref = f"ORDER_{uuid.uuid4().hex[:10].upper()}"

    # 3. Lưu lịch sử giao dịch trạng thái pending
    new_txn = Transactions(
        user_id=user_id,
        package_id=package.id,
        amount_paid=package.price,
        tokens_added=package.token,
        transaction_ref=txn_ref,
        status="pending"
    )
    db.add(new_txn)
    db.commit()

    # 4. Tạo URL VNPAY
    vnp_amount = str(int(package.price * 100))  # VNPAY yêu cầu nhân 100
    payment_data = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": settings.VNPAY_TMN_CODE,
        "vnp_Amount": vnp_amount,
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": txn_ref,
        "vnp_OrderInfo": f"Thanh toan goi {package.name}",
        "vnp_OrderType": "billpayment",
        "vnp_Locale": "vn",
        "vnp_CreateDate": datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        "vnp_IpAddr": client_ip,
        "vnp_ReturnUrl": settings.VNPAY_RETURN_URL
    }

    return vnpay.get_payment_url(payment_data)


def process_vnpay_return(db: Session, query_params: dict):
    if not vnpay.validate_response(query_params):
        return {"success": False, "message": "Sai chữ ký bảo mật VNPAY"}

    txn_ref = query_params.get("vnp_TxnRef")
    response_code = query_params.get("vnp_ResponseCode")

    # Lấy thêm các thông tin từ VNPAY
    vnp_transaction_no = query_params.get("vnp_TransactionNo")
    bank_code = query_params.get("vnp_BankCode")
    pay_date = query_params.get("vnp_PayDate")

    txn = db.query(Transactions).filter(
        Transactions.transaction_ref == txn_ref).first()

    if not txn:
        return {"success": False, "message": "Giao dịch không tồn tại"}

    if txn.status != "pending":
        return {"success": True, "message": "Giao dịch này đã được xử lý trước đó"}

    # Cập nhật thông tin chi tiết từ VNPAY vào transaction record
    txn.vnp_transaction_no = vnp_transaction_no
    txn.vnp_response_code = response_code
    txn.bank_code = bank_code
    txn.pay_date = pay_date

    if response_code == "00":  # Thành công
        txn.status = "success"

        # Cộng token cho user
        user_wallet = db.query(Tokens).filter(
            Tokens.user_id == txn.user_id).first()
        if user_wallet:
            user_wallet.balance += txn.tokens_added
        else:
            new_wallet = Tokens(user_id=txn.user_id, balance=txn.tokens_added)
            db.add(new_wallet)

        db.commit()
        return {"success": True, "message": "Giao dịch thành công", "tokens_added": txn.tokens_added}
    else:
        txn.status = "failed"
        db.commit()
        return {"success": False, "message": f"Giao dịch thất bại (Mã lỗi: {response_code})"}


def get_user_payment_history(db: Session, user_id: str, skip: int = 0, limit: int = 20):
    return db.query(Transactions).filter(Transactions.user_id == user_id)\
             .order_by(Transactions.created_at.desc())\
             .offset(skip).limit(limit).all()

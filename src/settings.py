from environs import Env
from loguru import logger


# log_file_format = "{time:YYYY-MM-DD}.log"
# logger.add(f"logging/{log_file_format}", rotation="00:00", retention="7 days", enqueue=True)


env = Env()
logger.info(f"Loading environment variables...")


# FASTAPI_ENVIRONMENT = env.str("FASTAPI_ENVIRONMENT", default="PRODUCTION")

PORT = env.int("PORT")
DATABASE_URL = env.str("DATABASE_URL")


SUPABASE_PROJECT_ID = env.str("SUPABASE_PROJECT_ID")
SUPABASE_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co"
JWKS_URL = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
ISSUER = f"{SUPABASE_URL}/auth/v1"
AUDIENCE = "authenticated"


VNPAY_TMN_CODE = env.str("VNPAY_TMN_CODE")
VNPAY_HASH_SECRET_KEY = env.str("VNPAY_HASH_SECRET_KEY")
VNPAY_RETURN_URL = env.str("VNPAY_RETURN_URL")
VNPAY_PAYMENT_URL = env.str("VNPAY_PAYMENT_URL")
VNPAY_API_URL = env.str("VNPAY_API_URL")


print("*" * 100)
for key, value in list(globals().items()):
    if key.isupper():
        # logger.info(f"{key}: {value}")
        logger.info(f"{key}: ***")
print("*" * 100)


print("=" * 100)
print(f"Application is running on: http://localhost:{PORT}/docs")
print(
    f"https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/authorize?provider=google")
print("=" * 100)

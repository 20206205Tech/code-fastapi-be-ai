from environs import Env
from loguru import logger


# log_file_format = "{time:YYYY-MM-DD}.log"
# logger.add(f"logging/{log_file_format}", rotation="00:00", retention="7 days", enqueue=True)


env = Env()
logger.info(f"Loading environment variables...")


# FASTAPI_ENVIRONMENT = env.str("FASTAPI_ENVIRONMENT", default="PRODUCTION")

PORT = env.int("PORT")
DATABASE_URL = env.str("DATABASE_URL")


for key, value in list(globals().items()):
    if key.isupper():
        # logger.info(f"{key}: {value}")
        logger.info(f"{key}: ***")


print("=" * 100)
print(f"http://localhost:{PORT}/docs")
print("=" * 100)

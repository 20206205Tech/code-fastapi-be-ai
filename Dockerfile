# ==========================================
# Bước 1: Builder stage
# ==========================================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Thiết lập môi trường để uv tối ưu bytecode và cache
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Cài đặt dependencies trước để tận dụng Docker cache hiệu quả
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy toàn bộ source code vào
COPY . /app

# Sync lại để cài đặt chính project hiện tại (không bao gồm dev dependencies)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ==========================================
# Bước 2: Runtime stage
# ==========================================
FROM python:3.12-slim-bookworm

# Ngăn Python tạo file .pyc và bật unbuffered logging để xem log Heroku realtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy môi trường ảo (.venv) từ builder sang
COPY --from=builder /app/.venv /app/.venv

# Copy thư mục mã nguồn
COPY ./src /app/src

# Thiết lập đường dẫn môi trường
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# Heroku sẽ tự động truyền biến PORT vào, set mặc định 8000 để nếu test local không bị lỗi
ENV PORT=8000

# Chú ý: Cần dùng `sh -c` để Uvicorn có thể đọc được biến môi trường ${PORT} do Heroku cấp phát
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
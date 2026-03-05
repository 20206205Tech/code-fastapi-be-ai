# # Bước 1: Build stage
# FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# # Thiết lập môi trường để uv không tạo file .pyc và tối ưu cache
# ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# WORKDIR /app

# # Copy file cấu hình trước để tận dụng Docker cache
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --frozen --no-install-project --no-dev

# # Copy mã nguồn vào
# ADD . /app

# # Sync lại để bao gồm cả project hiện tại
# RUN --mount=type=cache,target=/root/.cache/uv \
#     uv sync --frozen --no-dev


# # Bước 2: Runtime stage
# FROM python:3.12-slim-bookworm

# WORKDIR /app

# # Copy môi trường ảo (.venv) từ builder sang
# COPY --from=builder /app/.venv /app/.venv

# # Copy mã nguồn
# COPY . /app

# # Thêm .venv/bin vào PATH để chạy app không cần source
# ENV PATH="/app/.venv/bin:$PATH"

# # Chạy ứng dụng (Ví dụ với FastAPI/Uvicorn)
# CMD ["python", "app.py"]
from app.middlewares.log_request_and_response_middleware import LogRequestAndResponseMiddleware
# import settings
from fastapi import FastAPI
from index_router import index_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogRequestAndResponseMiddleware)


app.include_router(index_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Hello World",
        "docs": "/docs"
    }

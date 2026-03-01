import settings
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Hello World",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.IP, port=settings.PORT, reload=True)

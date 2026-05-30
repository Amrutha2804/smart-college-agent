from fastapi import FastAPI
from .routes import router
app = FastAPI(
    title="KIIT Smart College API",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

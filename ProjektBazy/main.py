from fastapi import FastAPI
from contextlib import asynccontextmanager
from tortoise.contrib.fastapi import register_tortoise
from user.controller import router as user_router
from db_init import create_default_admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_default_admin()
    yield

app = FastAPI(title="User Management API", lifespan=lifespan)

app.include_router(user_router, prefix="/api", tags=["api"])

register_tortoise(
    app,
    db_url="postgres://admin:samuel@localhost:5432/sklep",
    modules={"models": ["user.model"]},
    add_exception_handlers=True
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

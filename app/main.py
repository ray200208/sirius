from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine, Base
from app.routers import webhook
import logging

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (use Alembic migrations in production)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="SaaS Change Detection Engine",
    description="Monitors external sources for pricing, keyword, and messaging changes.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(webhook.router)


@app.get("/health")
async def health():
    return {"status": "ok"}

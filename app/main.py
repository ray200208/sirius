from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine, Base
from pydantic import BaseModel
from app.routers import webhook
from datetime import datetime
import logging
import subprocess

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

class ScrapedData(BaseModel):
    company: str
    url: str
    scraped_at: str
    headline: str
    subheadlines: list[str]
    cta_buttons: list[str]
    pricing_text: str
    full_text: str

@app.post("/ingest")
def ingest(data: ScrapedData):
    # 🔥 THIS IS WHERE YOUR PIPELINE CONTINUES

    # Example processing (P4 logic)
    profile = {
        "audience": "beginner" if "beginner" in data.full_text.lower() else "job-seeker",
        "pricing": "premium" if "100000" in data.pricing_text else "budget"
    }

    # Save to DB (or mock for now)
    return {
        "status": "success",
        "profile": profile
    }


@app.post("/rescrape")
def rescrape():
    try:
        # Go to scraper folder and run spiders
        subprocess.run(
            ["python", "-m", "scrapy", "crawl", "scaler", "-o", "../data/scaler_rescrape.json"],
            cwd="scraper"
        )

        subprocess.run(
            ["python", "-m", "scrapy", "crawl", "gfg", "-o", "../data/gfg_rescrape.json"],
            cwd="scraper"
        )

        return {"status": "rescrape completed"}

    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
async def health():
    return {"status": "ok"}

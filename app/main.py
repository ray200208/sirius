from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine, Base
from pydantic import BaseModel
from app.routers import webhook
from datetime import datetime
import logging
import subprocess
from fastapi.middleware.cors import CORSMiddleware

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # Node.js
        "http://localhost:5173",   # React Vite
        "http://localhost:5174",   # React alternate port
        "*",                       # open during hackathon
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


# ADD this right after app = FastAPI(...)


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

# ADD these routes to app/main.py

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EdgeIQ Python Backend"}

@app.get("/api/snapshots")
async def get_snapshots(db: AsyncSession = Depends(get_db)):
    # Query your existing snapshots/events table
    result = await db.execute(
        select(ChangeEvent).order_by(ChangeEvent.detected_at.desc()).limit(50)
    )
    events = result.scalars().all()
    return [
        {
            "source_id":   e.source_id,
            "source_type": e.source_type,
            "change_type": e.change_type,
            "severity":    e.severity,
            "detected_at": str(e.detected_at),
            "summary":     e.summary,
        }
        for e in events
    ]

@app.get("/api/sources")

# ADD these routes to app/main.py

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EdgeIQ Python Backend"}

@app.get("/api/snapshots")
async def get_snapshots(db: AsyncSession = Depends(get_db)):
    # Query your existing snapshots/events table
    result = await db.execute(
        select(ChangeEvent).order_by(ChangeEvent.detected_at.desc()).limit(50)
    )
    events = result.scalars().all()
    return [
        {
            "source_id":   e.source_id,
            "source_type": e.source_type,
            "change_type": e.change_type,
            "severity":    e.severity,
            "detected_at": str(e.detected_at),
            "summary":     e.summary,
        }
        for e in events
    ]

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EdgeIQ Python Backend"}

@app.get("/api/snapshots")
async def get_snapshots(db: AsyncSession = Depends(get_db)):
    # Query your existing snapshots/events table
    result = await db.execute(
        select(ChangeEvent).order_by(ChangeEvent.detected_at.desc()).limit(50)
    )
    events = result.scalars().all()
    return [
        {
            "source_id":   e.source_id,
            "source_type": e.source_type,
            "change_type": e.change_type,
            "severity":    e.severity,
            "detected_at": str(e.detected_at),
            "summary":     e.summary,
        }
        for e in events
    ]

@app.get("/api/sources")
async def get_sources(db: AsyncSession = Depends(get_db)):
    # Return list of unique tracked competitors
    result = await db.execute(
        select(ChangeEvent.source_id).distinct()
    )
    sources = result.scalars().all()
    return {"sources": sources}

# SaaS Change Detection Engine

Python · FastAPI · PostgreSQL · asyncpg

## Setup

```bash
cd saas_engine
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your DB credentials
uvicorn app.main:app --reload --port 8000
```

## Webhook payload format

POST to `http://localhost:8000/webhook/ingest`

```json
{
  "source_id": "competitor-a",
  "source_type": "pricing",
  "data": {
    "headline": "Affordable AI for every learner",
    "keywords": ["affordable", "ai", "exam", "skills"],
    "plans": [
      { "name": "starter", "price": "₹499/month", "features": ["5 exams", "AI hints"] },
      { "name": "pro",     "price": "₹999/month", "features": ["unlimited", "AI coaching"] }
    ]
  }
}
```

Headers:
```
x-webhook-secret: <your secret>
```

## What gets detected

| Detector | Triggers |
|---|---|
| **Price change** | Any plan price up/down ≥ 5% (configurable) |
| **Plan added/removed** | New or missing plan names |
| **Feature diff** | Added/removed feature strings per plan |
| **Keyword change** | Keywords added or removed from the list |
| **Headline change** | Primary messaging copy changed |
| **Anomaly** | Price Z-score ≥ 2.5σ from historical mean |

## Severity levels

`low` → `medium` → `high` → `critical`

Critical = price anomaly > 4σ or price change > 25%

## Query change history

```
GET /webhook/events/{source_id}?limit=50
```

## Node.js integration

When changes are detected, the engine POSTs to:
```
POST {NODE_API_URL}/internal/change-events
x-internal-secret: <your secret>
```
## Database Migrations (Alembic)
```bash
cd saas_engine
alembic revision --autogenerate -m "initial models"
alembic upgrade head
cd node
npm install
cp .env.example .env
npm run dev

'''
Node.js receives the payload and fans out to email/Slack as needed.

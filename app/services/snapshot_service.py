from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Any

from app.models.models import DataSnapshot, ChangeEvent, PriceHistory
from app.models.schemas import WebhookPayload, ChangeEventOut, ProcessResult
from app.services.change_detector import (
    detect_price_changes,
    detect_keyword_changes,
    detect_messaging_changes,
    detect_price_anomaly,
    ChangeResult,
)
from app.services.extractors import extract_price, extract_currency
import uuid


async def process_webhook(payload: WebhookPayload, db: AsyncSession) -> ProcessResult:
    """
    Main orchestrator:
      1. Save new snapshot
      2. Load previous snapshot for this source
      3. Run all detectors
      4. Persist change events
      5. Return structured result
    """
    # 1. Save snapshot
    snapshot = DataSnapshot(
        source_id=payload.source_id,
        source_type=payload.source_type,
        payload=payload.data,
    )
    db.add(snapshot)
    await db.flush()  # get the ID before commit

    # 2. Load previous snapshot
    result = await db.execute(
        select(DataSnapshot)
        .where(DataSnapshot.source_id == payload.source_id)
        .where(DataSnapshot.id != snapshot.id)
        .order_by(desc(DataSnapshot.created_at))
        .limit(1)
    )
    previous = result.scalar_one_or_none()

    all_changes: list[ChangeResult] = []

    if previous:
        old_data: dict[str, Any] = previous.payload
        new_data: dict[str, Any] = payload.data

        # 3a. Pricing changes
        old_plans = old_data.get("plans", [])
        new_plans = new_data.get("plans", [])
        if old_plans or new_plans:
            all_changes.extend(detect_price_changes(old_plans, new_plans))

        # 3b. Keyword changes
        old_kw = old_data.get("keywords", [])
        new_kw = new_data.get("keywords", [])
        context = new_data.get("headline", "") + " " + new_data.get("description", "")
        all_changes.extend(detect_keyword_changes(old_kw, new_kw, context))

        # 3c. Messaging / headline changes
        all_changes.extend(detect_messaging_changes(old_data, new_data))

    # 4. Save price history + run anomaly detection
    for plan in payload.data.get("plans", []):
        price = extract_price(str(plan.get("price", "")))
        currency = extract_currency(str(plan.get("price", "")))
        plan_name = plan.get("name", "unknown")

        if price is not None:
            ph = PriceHistory(
                source_id=payload.source_id,
                plan_name=plan_name,
                price=price,
                currency=currency,
            )
            db.add(ph)

            # Load history for anomaly check
            hist_result = await db.execute(
                select(PriceHistory.price)
                .where(PriceHistory.source_id == payload.source_id)
                .where(PriceHistory.plan_name == plan_name)
                .order_by(desc(PriceHistory.recorded_at))
                .limit(50)
            )
            history = [row[0] for row in hist_result.fetchall()] + [price]

            anomaly = detect_price_anomaly(plan_name, history, price)
            if anomaly:
                all_changes.append(anomaly)

    # 5. Persist change events
    event_rows: list[ChangeEvent] = []
    for change in all_changes:
        event = ChangeEvent(
            source_id=payload.source_id,
            change_type=change.change_type,
            severity=change.severity,
            description=change.description,
            diff=change.diff,
            old_value=change.old_value,
            new_value=change.new_value,
        )
        db.add(event)
        event_rows.append(event)

    await db.commit()

    return ProcessResult(
        source_id=payload.source_id,
        snapshot_id=snapshot.id,
        changes_detected=len(all_changes),
        events=[ChangeEventOut.model_validate(e) for e in event_rows],
    )


async def get_recent_events(
    source_id: str, limit: int, db: AsyncSession
) -> list[ChangeEventOut]:
    result = await db.execute(
        select(ChangeEvent)
        .where(ChangeEvent.source_id == source_id)
        .order_by(desc(ChangeEvent.created_at))
        .limit(limit)
    )
    return [ChangeEventOut.model_validate(r) for r in result.scalars().all()]

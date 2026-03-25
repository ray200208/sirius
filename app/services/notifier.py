import httpx
import logging
from app.models.schemas import ProcessResult
from app.config import settings

async def notify_node(result: ProcessResult):
    """Async fire-and-forget notification to your Node.js API."""
    if not settings.NODE_API_URL:
        logging.debug("NODE_API_URL not set → skipping Node.js notification")
        return

    if not settings.INTERNAL_SECRET:
        logging.warning("INTERNAL_SECRET missing → cannot notify Node.js")
        return

    url = f"{settings.NODE_API_URL.rstrip('/')}/internal/change-events"
    headers = {
        "x-internal-secret": settings.INTERNAL_SECRET,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            response = await client.post(
                url,
                json=result.model_dump(mode="json"),
                headers=headers,
            )
            if response.status_code >= 300:
                logging.error(
                    f"Node.js notification failed {response.status_code}: {response.text[:200]}"
                )
            else:
                logging.info(f"✅ Notified Node.js – {result.changes_detected} change(s)")
    except Exception as e:
        logging.error(f"Failed to notify Node.js: {e}")
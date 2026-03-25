// frontend/src/api.js  ← CREATE THIS FILE

const PYTHON_API = "http://localhost:8000"   // FastAPI
const NODE_API   = "http://localhost:3000"   // Node.js

async function safeFetch(url) {
  try {
    const res = await fetch(url)
    if (!res.ok) throw new Error(`${res.status}`)
    return await res.json()
  } catch (e) {
    console.error(`Failed: ${url}`, e.message)
    return null
  }
}

async function safePost(url, body) {
  try {
    const res = await fetch(url, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(body),
    })
    if (!res.ok) throw new Error(`${res.status}`)
    return await res.json()
  } catch (e) {
    console.error(`POST failed: ${url}`, e.message)
    return null
  }
}

// ── FROM PYTHON BACKEND ───────────────────────────────────────────────────────

export async function checkPythonHealth() {
  const data = await safeFetch(`${PYTHON_API}/health`)
  return data !== null
}

export async function getSnapshots() {
  return await safeFetch(`${PYTHON_API}/api/snapshots`) || []
}

export async function getSources() {
  const data = await safeFetch(`${PYTHON_API}/api/sources`)
  return data?.sources || []
}

export async function getChangeHistory(sourceId) {
  return await safeFetch(
    `${PYTHON_API}/webhook/events/${sourceId}?limit=50`
  ) || []
}

// Send scraper data directly to Python webhook
export async function ingestScraperData(sourceId, sourceType, data) {
  return await safePost(`${PYTHON_API}/webhook/ingest`, {
    source_id:   sourceId,
    source_type: sourceType,
    data:        data,
  })
}

// ── FROM NODE.JS LAYER ────────────────────────────────────────────────────────

export async function checkNodeHealth() {
  const data = await safeFetch(`${NODE_API}/health`)
  return data !== null
}

export async function getRecentEvents() {
  return await safeFetch(`${NODE_API}/api/events`) || []
}

export async function getEventsBySource(sourceId) {
  return await safeFetch(`${NODE_API}/api/events/${sourceId}`) || []
}

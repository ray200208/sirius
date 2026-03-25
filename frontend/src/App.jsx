// frontend/src/App.jsx
// ADD these imports at the very top

import { useEffect, useState } from "react"
import {
  checkPythonHealth,
  checkNodeHealth,
  getSnapshots,
  getSources,
  getRecentEvents,
  getChangeHistory,
  ingestScraperData,
} from "./api.js"

// Then in your component, replace any hardcoded data with:

export default function App() {
  const [pythonOk,  setPythonOk]  = useState(null)
  const [nodeOk,    setNodeOk]    = useState(null)
  const [snapshots, setSnapshots] = useState([])
  const [sources,   setSources]   = useState([])
  const [events,    setEvents]    = useState([])
  const [loading,   setLoading]   = useState(true)

  useEffect(() => {
    loadAll()
  }, [])

  async function loadAll() {
    setLoading(true)

    // Check both services
    const [py, node] = await Promise.all([
      checkPythonHealth(),
      checkNodeHealth(),
    ])
    setPythonOk(py)
    setNodeOk(node)

    // Load data in parallel
    const [snaps, srcs, evts] = await Promise.all([
      getSnapshots(),
      getSources(),
      getRecentEvents(),
    ])
    setSnapshots(snaps)
    setSources(srcs)
    setEvents(evts)
    setLoading(false)
  }

  // ... rest of your existing JSX
  // Just replace wherever you had hardcoded data with:
  // snapshots, sources, events from state above
}

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Overview from "./pages/Overview";
import Insights from "./pages/Insights";
import Changes from "./pages/Changes";
import AskAI from "./pages/AskAI";
import DomainSelect from "./pages/DomainSelect";

function App() {
  return (
    <div  style={{
    fontFamily: "Arial, sans-serif",
    padding: "20px",
    backgroundColor: "#0f172a",
    minHeight: "100vh",
    color: "white",
  }}>
      <BrowserRouter>
        <Routes>
  <Route path="/" element={<DomainSelect />} />
  <Route path="/overview" element={<Overview />} />
  <Route path="/insights" element={<Insights />} />
  <Route path="/changes" element={<Changes />} />
  <Route path="/ask" element={<AskAI />} />
</Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

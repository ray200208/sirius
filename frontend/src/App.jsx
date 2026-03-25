import { BrowserRouter, Routes, Route } from "react-router-dom";
import Overview from "./pages/Overview";
import Insights from "./pages/Insights";
import Changes from "./pages/Changes";
import AskAI from "./pages/AskAI";

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
          <Route path="/" element={<Overview />} />
          <Route path="/insights" element={<Insights />} />
          <Route path="/changes" element={<Changes />} />
          <Route path="/ask" element={<AskAI />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
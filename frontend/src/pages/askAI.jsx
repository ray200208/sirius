import Navbar from "../components/Navbar";
import { useState } from "react";

function AskAI() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = () => {
  if (!question) {
    setAnswer("Please enter a question first.");
  } else {
    setAnswer(`Insight: ${question} → Competitors focus on short courses.`);
  }
};

  return (
    <div>
      <Navbar />
      <h2>Ask AI</h2>

    <input
  type="text"
  placeholder="Ask a question..."
  value={question}
  onChange={(e) => setQuestion(e.target.value)}
  style={{
    padding: "10px",
    width: "300px",
    marginRight: "10px",
    borderRadius: "5px",
    backgroundColor: "#020617",
    color: "white",
    border: "1px solid #334155",
  }}
/>

<button
  onClick={handleAsk}
  style={{
    padding: "10px",
    backgroundColor: "#2563eb",
    color: "white",
    border: "none",
    borderRadius: "5px",
  }}
>
  Ask
</button>


      {answer && (
        <div
          style={{
            marginTop: "20px",
            backgroundColor: "#1e293b",
color: "white",
            padding: "15px",
            borderRadius: "10px",
          }}
        >
          {answer}
        </div>
      )}
    </div>
  );
}

export default AskAI;
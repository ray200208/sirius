import Navbar from "../components/Navbar";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Overview() {
  const [company, setCompany] = useState("");
  const [competitors, setCompetitors] = useState("");
  const [url, setUrl] = useState("");

  const navigate = useNavigate();

  // Get selected domain
  const domain = localStorage.getItem("domain");

 const handleSubmit = () => {
  console.log("Button clicked");

  if (!company || !url || !competitors) {
    alert("Please fill all fields");
    return;
  }

  // Store data for other pages
  localStorage.setItem("competitors", competitors);
  localStorage.setItem("company", company);
  localStorage.setItem("url", url);

  console.log("Domain:", domain);
  console.log("Company:", company);
  console.log("Competitors:", competitors);
  console.log("Website:", url);

  // Navigate to insights page
  navigate("/insights");
};

  return (
    <div>
      <Navbar />

      <h1>EdTech Intelligence Dashboard</h1>

      {/* Show selected domain */}
      <p>
        Selected Domain: <b>{domain}</b>
      </p>

      {/* Input Section */}
      <div
        style={{
          backgroundColor: "#1e293b",
          padding: "20px",
          borderRadius: "10px",
          marginTop: "20px",
          width: "350px",
        }}
      >
        <h3>Enter Your Company Details</h3>

        <input
          type="text"
          placeholder="Company Name"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          style={{
            display: "block",
            margin: "10px 0",
            padding: "10px",
            width: "100%",
            backgroundColor: "#020617",
            color: "white",
            border: "1px solid #334155",
            borderRadius: "5px",
          }}
        />

        <input
          type="text"
          placeholder="Website URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{
            display: "block",
            margin: "10px 0",
            padding: "10px",
            width: "100%",
            backgroundColor: "#020617",
            color: "white",
            border: "1px solid #334155",
            borderRadius: "5px",
          }}
        />
        <input
  type="text"
  placeholder="Competitor Names (comma separated)"
  value={competitors}
  onChange={(e) => setCompetitors(e.target.value)}
  style={{
    display: "block",
    margin: "10px 0",
    padding: "10px",
    width: "100%",
    backgroundColor: "#020617",
    color: "white",
    border: "1px solid #334155",
    borderRadius: "5px",
  }}
/>

        <button
          onClick={handleSubmit}
          style={{
            padding: "10px",
            backgroundColor: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: "5px",
            marginTop: "10px",
            width: "100%",
            cursor: "pointer",
          }}
        >
          Analyze
        </button>
      </div>
    </div>
  );
}

export default Overview;
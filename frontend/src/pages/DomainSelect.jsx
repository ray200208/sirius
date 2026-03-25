import { useNavigate } from "react-router-dom";

function DomainSelect() {
  const navigate = useNavigate();

  const handleSelect = (domain) => {
    localStorage.setItem("domain", domain);
    navigate("/overview");
  };

  return (
    <div
      style={{
        backgroundColor: "#0f172a",
        minHeight: "100vh",
        color: "white",
        padding: "40px",
      }}
    >
      <h1>Select Your Domain</h1>

      <div style={{ display: "flex", gap: "20px", marginTop: "30px" }}>
        <button onClick={() => handleSelect("Competitive Exams")} style={btnStyle}>
          Competitive Exams
        </button>

        <button onClick={() => handleSelect("Technical Courses")} style={btnStyle}>
          Technical Courses
        </button>

        <button onClick={() => handleSelect("Schools & Colleges")} style={btnStyle}>
          Schools & Colleges
        </button>
      </div>
    </div>
  );
}

const btnStyle = {
  padding: "20px",
  backgroundColor: "#1e293b",
  color: "white",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer",
};

export default DomainSelect;
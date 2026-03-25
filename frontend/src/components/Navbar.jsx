import { Link } from "react-router-dom";

function Navbar() {
  return (
    <div
      style={{
        display: "flex",
        gap: "30px",
        padding: "15px",
        backgroundColor: "#020617",
        color: "white",
        borderRadius: "10px",
        marginBottom: "20px",
      }}
    >
      <Link to="/" style={{ color: "white", textDecoration: "none" }}>Overview</Link>
      <Link to="/insights" style={{ color: "white", textDecoration: "none" }}>Insights</Link>
      <Link to="/changes" style={{ color: "white", textDecoration: "none" }}>Changes</Link>
      <Link to="/ask" style={{ color: "white", textDecoration: "none" }}>Ask AI</Link>
    </div>
  );
}

export default Navbar;
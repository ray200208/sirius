import Navbar from "../components/Navbar";

function Overview() {
  return (
    <div>
      <Navbar />
      <h1>EdTech Intelligence Dashboard</h1>

      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
        <div style={{ padding: "20px", background: "#1e293b", borderRadius: "10px" }}>
          Competitors Tracked: 3
        </div>

        <div style={{ padding: "20px", background: "#1e293b", borderRadius: "10px" }}>
          Insights Generated: 5
        </div>
      </div>
    </div>
  );
}

export default Overview;
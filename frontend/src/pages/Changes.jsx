import Navbar from "../components/Navbar";

function Changes() {
  const changes = [
    "Scaler increased pricing",
    "GFG launched new course",
    "New discount offer added",
  ];

  return (
    <div>
      <Navbar />
      <h2>Recent Changes</h2>

      {changes.map((change, index) => (
        <div
          key={index}
          style={{
  backgroundColor: "#1e293b",
  padding: "15px",
  borderRadius: "10px",
  margin: "10px 0",
}}
        >
          {change}
        </div>
      ))}
    </div>
  );
}

export default Changes;
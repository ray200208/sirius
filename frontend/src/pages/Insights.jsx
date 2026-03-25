import Navbar from "../components/Navbar";

function Insights() {
  const insights = [
    "Short courses are getting more enrollments",
    "YouTube classes increase engagement",
    "Competitors are increasing prices",
  ];

  return (
    <div>
      <Navbar />
      <h2>Insights</h2>

      {insights.map((item, index) => (
        <div key={index} style={{
  backgroundColor: "#1e293b",
  padding: "15px",
  borderRadius: "10px",
  margin: "10px 0",
  boxShadow: "0 2px 5px rgba(0,0,0,0.5)",
}}>
          <p>{item}</p>
        </div>
      ))}
    </div>
  );
}

export default Insights;
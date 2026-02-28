import { useState, useEffect } from "react";
import { workflowAPI } from "./services/api";

export default function App() {
  const [workflows, setWorkflows] = useState([]);
  const [name, setName] = useState("");
  const [inputData, setInputData] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadWorkflows();
  }, []);

  const loadWorkflows = async () => {
    try {
      const res = await workflowAPI.list();
      setWorkflows(res.data);
    } catch (err) {
      console.error("Failed to load workflows:", err);
    }
  };

  const triggerWorkflow = async () => {
    if (!name || !inputData) {
      setMessage("⚠️ Please fill in both fields.");
      return;
    }
    setLoading(true);
    setMessage("");
    try {
      const res = await workflowAPI.create(name, inputData);
      setMessage(`✅ Workflow triggered! ID: ${res.data.id}`);
      setName("");
      setInputData("");
      loadWorkflows();
    } catch (err) {
      setMessage(`❌ Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: "sans-serif", maxWidth: 800, margin: "40px auto", padding: "0 20px" }}>
      <h1>🤖 AI Workflow Automation</h1>

      <div style={{ background: "#f5f5f5", padding: 20, borderRadius: 8, marginBottom: 30 }}>
        <h2>Trigger New Workflow</h2>
        <input
          placeholder="Workflow name (e.g., 'Process Customer Email')"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ width: "100%", padding: 8, marginBottom: 10, boxSizing: "border-box" }}
        />
        <textarea
          placeholder="Input data for AI to process..."
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          rows={4}
          style={{ width: "100%", padding: 8, marginBottom: 10, boxSizing: "border-box" }}
        />
        <button
          onClick={triggerWorkflow}
          disabled={loading}
          style={{ background: "#4F46E5", color: "white", padding: "10px 20px", border: "none", borderRadius: 6, cursor: "pointer" }}
        >
          {loading ? "Processing..." : "Run Workflow"}
        </button>
        {message && <p style={{ marginTop: 10 }}>{message}</p>}
      </div>

      <h2>Recent Workflows</h2>
      {workflows.length === 0 ? (
        <p>No workflows yet. Trigger one above!</p>
      ) : (
        workflows.map((w) => (
          <div key={w.id} style={{ border: "1px solid #ddd", padding: 15, borderRadius: 8, marginBottom: 10 }}>
            <strong>{w.name}</strong>
            <span style={{ marginLeft: 10, color: w.status === "completed" ? "green" : "orange" }}>
              {w.status}
            </span>
            <p style={{ color: "#666", fontSize: 13 }}>{new Date(w.created_at).toLocaleString()}</p>
          </div>
        ))
      )}
    </div>
  );
}

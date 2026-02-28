import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

export const workflowAPI = {
  // Create a new workflow
  create: (name, inputData) =>
    api.post("/api/workflows/", { name, input_data: inputData }),

  // Get all workflows
  list: () => api.get("/api/workflows/"),

  // Get a specific workflow
  get: (id) => api.get(`/api/workflows/${id}`),
};

export default api;

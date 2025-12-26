import axios from "axios";

const API_BASE = "";

export async function fetchJobs(keyword, signal) { // Added signal parameter
  try {
    // Pass the keyword as 'query' param if it exists
    const params = keyword ? { query: keyword } : {};
    
    const res = await axios.get(`${API_BASE}/jobs/`, {
      params,
      timeout: 30000, // Increased timeout for potentially slower AI responses
      signal, // Pass the AbortSignal to axios
    });

    // The backend now returns a consistent shape with an 'ai_powered' flag
    return res.data || { jobs: [], stats: {}, ai_powered: false };

  } catch (err) {
    // If the request was cancelled, do not log an error
    if (axios.isCancel(err)) {
      console.log("Fetch request cancelled:", err.message);
    } else {
      console.error("fetchJobs error:", err);
    }
    // Return a response shape consistent with the success case
    return { jobs: [], stats: {}, ai_powered: false };
  }
}



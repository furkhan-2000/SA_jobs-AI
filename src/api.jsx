import axios from "axios";

const API_BASE = "";

export async function fetchJobs(params = {}) {
  try {
    const res = await axios.get(`${API_BASE}/jobs/`, {
      params: {},
      timeout: 20000
    });
    return res.data || { jobs: [], stats: {}, count: 0 };
  } catch (err) {
    console.error("fetchJobs error", err);
    return { jobs: [], stats: {}, count: 0 };
  }
}

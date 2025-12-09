import axios from "axios";

const API_BASE = (window.__API_BASE__ && window.__API_BASE__.backend) || "http://localhost:7070";

export async function fetchJobs(params = {}) {
  try {
    const res = await axios.get(`${API_BASE}/jobs/`, {
      params: {
        keyword: params.keyword || undefined,
        job_type: params.job_type || undefined,
        industry: params.industry || undefined,
        page: params.page || 1,
        page_size: params.page_size || 20
      },
      timeout: 20000
    });
    return res.data || { jobs: [], stats: {}, count: 0 };
  } catch (err) {
    console.error("fetchJobs error", err);
    return { jobs: [], stats: {}, count: 0 };
  }
}

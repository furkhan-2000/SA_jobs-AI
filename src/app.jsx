import React, { useEffect, useState, useMemo } from "react";
import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import SearchFilter from "./components/SearchFilter.jsx";
import JobList from "./components/JobList.jsx";
// Pagination is removed as per client-side filtering
// import Pagination from "./components/Pagination.jsx";
import { fetchJobs } from "./api";

export default function App() {
  const [allFetchedJobs, setAllFetchedJobs] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [keyword, setKeyword] = useState("");
  // Pagination states removed: page, pageSize, total

  async function loadAllJobs() {
    setLoading(true);
    try {
      const res = await fetchJobs(); // No pagination params sent
      setAllFetchedJobs(res.jobs || []);
      setStats(res.stats || {});
      // total state removed
    } catch (error) {
      console.error("Error loading jobs:", error);
      setAllFetchedJobs([]);
      setStats({});
    } finally {
      setLoading(false);
    }
  }

  // Fetch all jobs on initial load
  useEffect(() => {
    loadAllJobs();
  }, []); // Empty dependency array means this runs once on mount

  // Client-side filtering based on keyword
  const filteredJobs = useMemo(() => {
    if (!keyword) {
      return allFetchedJobs;
    }
    const lowerKeyword = keyword.toLowerCase();
    return allFetchedJobs.filter(job =>
      (job.title || "").toLowerCase().includes(lowerKeyword) ||
      (job.company || "").toLowerCase().includes(lowerKeyword) ||
      (job.description || "").toLowerCase().includes(lowerKeyword)
    );
  }, [allFetchedJobs, keyword]);

  return (
    <div className="app">
      <Header />
      <main className="container">
        <SearchFilter
          keyword={keyword}
          setKeyword={setKeyword}
          // onSearch no longer needs to setPage(1) as filtering is client-side
          onSearch={() => { /* Filtering happens automatically on keyword change */ }}
        />
        <div className="content">
          <div className="left">
            {loading ? (
              <div className="loading">Loading…</div>
            ) : filteredJobs.length === 0 ? (
              <div className="no-results">
                No jobs found matching your search. Try a different keyword.
              </div>
            ) : (
              <JobList jobs={filteredJobs} />
            )}
            {/* Pagination component removed */}
          </div>
          <aside className="right">
            <div className="card stats">
              <h3>Analytics</h3>
              {/* Stats now reflect allFetchedJobs (before client-side filtering) */}
              <div>Total jobs (found by APIs): {stats.total_jobs || 0}</div>
              <div style={{ marginTop: 8 }}>
                <strong>Top companies</strong>
                <ul className="compact-list">
                  {Object.entries(stats.jobs_per_company || {})
                    .slice(0, 6)
                    .map(([k, v]) => (
                      <li key={k}>
                        {k} — {v}
                      </li>
                    ))}
                </ul>
              </div>
            </div>
          </aside>
        </div>
      </main>
      <Footer />
    </div>
  );
}
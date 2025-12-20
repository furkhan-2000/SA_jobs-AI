import React, { useEffect, useState } from "react";
import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import SearchFilter from "./components/SearchFilter.jsx";
import JobList from "./components/JobList.jsx";
import Pagination from "./components/Pagination.jsx";
import { fetchJobs } from "./api";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [keyword, setKeyword] = useState("");
  const [jobType, setJobType] = useState("");
  const [industry, setIndustry] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [total, setTotal] = useState(0);

  async function load() {
    setLoading(true);
    try {
      const res = await fetchJobs({
        keyword,
        job_type: jobType,
        industry,
        page,
        page_size: pageSize,
      });
      setJobs(res.jobs || []);
      setStats(res.stats || {});
      setTotal(res.count || 0);
    } catch (error) {
      console.error("Error loading jobs:", error);
      setJobs([]);
      setStats({});
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }

  // Effect for page changes - runs on mount and when page changes
  useEffect(() => {
    load();
  }, [page]);

  // Effect for filter changes - resets to page 1 and loads
  useEffect(() => {
    if (page === 1) {
      load();
    } else {
      setPage(1);
    }
  }, [keyword, jobType, industry]);

  return (
    <div className="app">
      <Header />
      <main className="container">
        <SearchFilter
          keyword={keyword}
          setKeyword={setKeyword}
          jobType={jobType}
          setJobType={setJobType}
          industry={industry}
          setIndustry={setIndustry}
          onSearch={() => {
            setPage(1);
            load();
          }}
        />
        <div className="content">
          <div className="left">
            {loading ? (
              <div className="loading">Loading…</div>
            ) : jobs.length === 0 ? (
              <div className="no-results">
                No jobs found. Try adjusting your search filters.
              </div>
            ) : (
              <JobList jobs={jobs} />
            )}
            <Pagination
              page={page}
              setPage={setPage}
              total={total}
              pageSize={pageSize}
            />
          </div>
          <aside className="right">
            <div className="card stats">
              <h3>Analytics</h3>
              <div>Total jobs: {stats.total_jobs || 0}</div>
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
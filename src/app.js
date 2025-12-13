import React, { useEffect, useState } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import SearchFilter from "./components/SearchFilter";
import JobList from "./components/JobList";
import Pagination from "./components/Pagination";
import { fetchJobs } from "./api";

export default function App(){
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [keyword, setKeyword] = useState("");
  const [jobType, setJobType] = useState("");
  const [industry, setIndustry] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [total, setTotal] = useState(0);

  async function load(){
    setLoading(true);
    const res = await fetchJobs({ keyword, job_type: jobType, industry, page, page_size: pageSize });
    setJobs(res.jobs || []);
    setStats(res.stats || {});
    setTotal(res.count || 0);
    setLoading(false);
  }

  useEffect(()=>{ load(); }, [keyword, jobType, industry, page]);

  return (
    <div className="app">
      <Header />
      <main className="container">
        <SearchFilter
          keyword={keyword} setKeyword={setKeyword}
          jobType={jobType} setJobType={setJobType}
          industry={industry} setIndustry={setIndustry}
          onSearch={()=>{ setPage(1); load(); }}
        />
        <div className="content">
          <div className="left">
            {loading ? <div className="loading">Loading…</div> :
              <JobList jobs={jobs} />
            }
            <Pagination page={page} setPage={setPage} total={total} pageSize={pageSize} />
          </div>
          <aside className="right">
            <div className="card stats">
              <h3>Analytics</h3>
              <div>Total jobs: {stats.total_jobs || 0}</div>
              <div style={{marginTop:8}}>
                <strong>Top companies</strong>
                <ul className="compact-list">
                  {Object.entries(stats.jobs_per_company || {}).slice(0,6).map(([k,v]) => <li key={k}>{k} — {v}</li>)}
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

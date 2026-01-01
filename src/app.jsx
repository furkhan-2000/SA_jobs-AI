import React, { useEffect, useState, useMemo, useRef } from "react";
import SearchFilter from "./components/SearchFilter.jsx";
import JobList from "./components/JobList.jsx";
import { fetchJobs } from "./api";

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);
  return debouncedValue;
}

export default function App() {
  const [masterJobList, setMasterJobList] = useState([]);
  const [displayJobs, setDisplayJobs] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [isAiPowered, setIsAiPowered] = useState(false);
  const [keyword, setKeyword] = useState("");
  const [jobTypeFilter, setJobTypeFilter] = useState("On-site KSA");
  const debouncedKeyword = useDebounce(keyword, 500);
  const searchIdRef = useRef(0);

  async function loadInitialJobs() {
    console.log("LOG: Initializing - fetching master job list.");
    setLoading(true);
    try {
      const res = await fetchJobs();
      setMasterJobList(res.jobs || []);
      setDisplayJobs(res.jobs || []);
      setStats(res.stats || {});
      setIsAiPowered(false);
      console.log(`LOG: Master job list loaded with ${res.jobs?.length || 0} jobs.`);
    } catch (error) {
      console.error("Error loading initial jobs:", error);
      setMasterJobList([]);
      setDisplayJobs([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadInitialJobs();
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    searchIdRef.current += 1;
    const currentSearchId = searchIdRef.current;

    const performSearch = async () => {
      if (debouncedKeyword) {
        console.log(`LOG: Debounced search triggered for keyword: '${debouncedKeyword}'`);
        setLoading(true);
        try {
          const res = await fetchJobs(debouncedKeyword, controller.signal);
          if (currentSearchId === searchIdRef.current) {
            setDisplayJobs(res.jobs || []);
            setStats(res.stats || {});
            setIsAiPowered(res.ai_powered);
            console.log(`LOG: Search complete. AI powered: ${res.ai_powered}. Found ${res.jobs?.length} jobs.`);
          } else {
            console.log("LOG: Stale search result ignored.");
          }
        } catch (error) {
          if (error.name === 'CanceledError') {
            console.log("LOG: Fetch aborted:", error.message);
          } else {
            console.error("Error during search:", error);
            setDisplayJobs(masterJobList);
            setIsAiPowered(false);
          }
        } finally {
          setLoading(false);
        }
      } else {
        console.log("LOG: Search box cleared. Resetting to master list (no network call).");
        setDisplayJobs(masterJobList);
        setIsAiPowered(false);
      }
    };

    performSearch();

    return () => {
      console.log("LOG: Aborting previous fetch request (cleanup).");
      controller.abort();
    };

  }, [debouncedKeyword, masterJobList]);

  const finalFilteredJobs = useMemo(() => {
    if (isAiPowered) {
        return displayJobs;
    }

    console.log("LOG: Applying client-side filters (Job Type) for fallback mode.");
    return displayJobs.filter(job => {
      const jobTypeMatch = !jobTypeFilter || (job.jobCategory === jobTypeFilter);
      return jobTypeMatch;
    });
  }, [displayJobs, jobTypeFilter, isAiPowered]);

  return (
    <div className="relative flex flex-col min-h-screen overflow-hidden">
      <main className="flex-grow container mx-auto p-4 pt-8 max-w-7xl">
        <SearchFilter
          keyword={keyword}
          setKeyword={setKeyword}
          jobTypeFilter={jobTypeFilter}
          setJobTypeFilter={setJobTypeFilter}
        />
        <div className="flex flex-col md:flex-row gap-4 mt-4">
          <div className="flex-grow">
            {loading ? (
              <div className="text-center text-gray-600">Loading…</div>
            ) : finalFilteredJobs.length === 0 ? (
              <div className="text-center text-gray-600">
                No jobs found matching your criteria.
              </div>
            ) : (
              <JobList jobs={finalFilteredJobs} />
            )}
          </div>
          <aside className="md:w-1/4">
            <div className="card glass-ui p-4 rounded-lg">
              <h3 className="font-bold text-lg mb-2 text-gray-800">Analytics</h3>
              <div className="text-gray-700">Total jobs (found by APIs): {stats.total_jobs || 0}</div>
              <div className="mt-2">
                <strong className="text-gray-800">Top companies</strong>
                <ul className="text-gray-700 text-sm">
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
    </div>
  );
}
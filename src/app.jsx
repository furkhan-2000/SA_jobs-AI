import React, { useEffect, useState, useMemo } from "react";
import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import SearchFilter from "./components/SearchFilter.jsx";
import JobList from "./components/JobList.jsx";
import SkeletonJobList from "./components/SkeletonJobList.jsx";
import { fetchJobs } from "./api";

// This custom hook handles the debouncing logic.
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    // Cleanup function to cancel the timeout if value changes
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);
  return debouncedValue;
}

export default function App() {
  // State for the full, original list of jobs. This is our "source of truth".
  const [masterJobList, setMasterJobList] = useState([]);
  // State for the jobs currently being displayed. Can be AI-filtered or the master list.
  const [displayJobs, setDisplayJobs] = useState([]);
  
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [isAiPowered, setIsAiPowered] = useState(false);

  // Live user input states
  const [keyword, setKeyword] = useState("");
  const [jobTypeFilter, setJobTypeFilter] = useState("");
  const [locationFilter, setLocationFilter] = useState("");

  // Debounced keyword state. This will only update after the user stops typing.
  const debouncedKeyword = useDebounce(keyword, 500);

  // 1. Fetches the initial master list of all jobs on component mount.
  async function loadInitialJobs() {
    console.log("LOG: Initializing - fetching master job list.");
    setLoading(true);
    try {
      const res = await fetchJobs(); // No search query
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

  // 2. This effect runs once on mount to load the initial data.
  useEffect(() => {
    loadInitialJobs();
  }, []);

  // 3. This effect watches for changes in the DEBOUNCED keyword.
  useEffect(() => {
    // This is the main search logic trigger.
    const performSearch = async () => {
      if (debouncedKeyword) {
        console.log(`LOG: Debounced search triggered for keyword: '${debouncedKeyword}'`);
        setLoading(true);
        try {
          const res = await fetchJobs(debouncedKeyword);
          setDisplayJobs(res.jobs || []);
          setStats(res.stats || {});
          setIsAiPowered(res.ai_powered);
          console.log(`LOG: Search complete. AI powered: ${res.ai_powered}. Found ${res.jobs?.length} jobs.`);
        } catch (error) {
          console.error("Error during search:", error);
          setDisplayJobs(masterJobList); // On error, fall back to master list
          setIsAiPowered(false);
        } finally {
          setLoading(false);
        }
      } else {
        // If the search box is cleared, reset to the master list instantly.
        console.log("LOG: Search box cleared. Resetting to master list (no network call).");
        setDisplayJobs(masterJobList);
        setIsAiPowered(false);
      }
    };
    
    performSearch();
    
  }, [debouncedKeyword]); // This effect ONLY runs when the debounced keyword changes.

  // 4. This final filtering step applies the dropdown filters (Job Type, Location).
  const finalFilteredJobs = useMemo(() => {
    // If AI is active, we assume the AI has already done the best filtering,
    // so we don't apply the simple dropdown filters on top.
    if (isAiPowered) {
        return displayJobs;
    }

    // In fallback mode, apply the local filters for type and location.
    // The keyword filter is already effectively applied by the debounced search.
    console.log("LOG: Applying client-side filters (Job Type, Location) for fallback mode.");
    return displayJobs.filter(job => {
      const keywordMatch = !debouncedKeyword ||
        (job.title || "").toLowerCase().includes(debouncedKeyword.toLowerCase()) ||
        (job.company || "").toLowerCase().includes(debouncedKeyword.toLowerCase()) ||
        (job.description || "").toLowerCase().includes(debouncedKeyword.toLowerCase());

      const jobTypeMatch = !jobTypeFilter || (job.jobType || "").toLowerCase().includes(jobTypeFilter.toLowerCase());
      const locationMatch = !locationFilter || (job.location || "").toLowerCase().includes(locationFilter.toLowerCase());
      return keywordMatch && jobTypeMatch && locationMatch;
    });
  }, [displayJobs, jobTypeFilter, locationFilter, isAiPowered, debouncedKeyword]);


  return (
    <div className="app">
      <Header />
      <main className="container">
        <SearchFilter
          keyword={keyword}
          setKeyword={setKeyword}
          jobTypeFilter={jobTypeFilter}
          setJobTypeFilter={setJobTypeFilter}
          locationFilter={locationFilter}
          setLocationFilter={setLocationFilter}
          jobTypes={Object.keys(stats.jobs_per_type || {})}
          locations={Object.keys(stats.jobs_per_location || {})}
          // The onSearch prop is no longer needed as search is automatic.
        />
        <div className="content">
          <div className="left">
            {loading ? (
              <SkeletonJobList count={5} />
            ) : finalFilteredJobs.length === 0 ? (
              <div className="no-results">
                No jobs found matching your criteria.
              </div>
            ) : (
              <JobList jobs={finalFilteredJobs} />
            )}
          </div>
          <aside className="right">
            <div className="card stats">
              <h3>Analytics</h3>
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
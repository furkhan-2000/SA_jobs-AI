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
        <div className="mt-4">
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
        </div>
      </main>
    </div>
  );
}
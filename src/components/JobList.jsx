import React from "react";
import JobCard from "./JobCard";

export default function JobList({ jobs }) {
  return (
    <div className="job-list">
      {jobs.map((job, i) => (
        <JobCard key={job.dedup_key} job={job} />
      ))}
    </div>
  );
}

import React from "react";
import JobCard from "./JobCard";

export default function JobList({ jobs }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {jobs.map((job) => (
        <JobCard key={job.dedup_key} job={job} />
      ))}
    </div>
  );
}
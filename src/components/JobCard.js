import React from "react";

export default function JobCard({ job }) {
  return (
    <div className="job-card">
      <h3>{job.title}</h3>
      <p>{job.company}</p>
      <p>{job.location}</p>
      <a href={job.url} target="_blank" rel="noopener noreferrer">
        View Job
      </a>
    </div>
  );
}

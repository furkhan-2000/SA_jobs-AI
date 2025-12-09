import React from "react";

export default function JobCard({ job }) {
    return (
        <div className="job-card">
            <div className="job-title">{job.title}</div>
            <div className="job-company">{job.company || "Unknown Company"}</div>
            <div>{job.location || "Location not provided"}</div>
            <a href={job.url} target="_blank" rel="noopener noreferrer">View Job</a>
        </div>
    );
}

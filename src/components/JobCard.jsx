import React from 'react';

export default function JobCard({ job }) {
    return (
        <div className="job-card">
            <div className="job-card-header">
                <h3 className="job-title">{job.title}</h3>
                <p className="job-company">{job.company}</p>
            </div>
            <div className="job-card-details">
                <span className="job-location">{job.location}</span>
                {job.jobType && <span className="badge job-type-badge">{job.jobType}</span>}
                {job.remote && <span className="badge remote-badge">Remote</span>}
            </div>
            <div className="job-card-footer">
                <a href={job.url} target="_blank" rel="noopener noreferrer" className="job-link-button">
                    View Job
                </a>
                <span className="job-source">Source: {job.source}</span>
            </div>
        </div>
    );
}

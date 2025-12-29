import React from "react";

export default function JobCard({ job }) {
  return (
    <div className="job-card glass-ui p-6 rounded-xl transition-all duration-300 ease-in-out hover:shadow-xl hover:-translate-y-1 flex flex-col justify-between h-full">
      <div className="job-card-header">
        <h3 className="text-xl font-bold text-gray-800 mb-2">{job.title}</h3>
        <p className="text-gray-700 text-base mb-1">{job.company}</p>
      </div>
      <div className="job-card-details flex flex-wrap gap-2 my-3">
        <span className="text-gray-600 text-sm">{job.location}</span>
        {job.jobType && (
          <span className="badge job-type-badge bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full text-xs font-semibold">
            {job.jobType}
          </span>
        )}
        {job.remote && (
          <span className="badge remote-badge bg-green-100 text-green-800 px-2 py-0.5 rounded-full text-xs font-semibold">
            Remote
          </span>
        )}
      </div>
      <div className="job-card-footer flex justify-between items-center mt-4">
        <a
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block px-5 py-2 bg-gray-800 text-white font-semibold rounded-full shadow-md hover:bg-gray-700 transition-colors duration-200 text-sm"
        >
          View Job
        </a>
        <span className="job-source text-xs text-gray-500">Source: {job.source}</span>
      </div>
    </div>
  );
}
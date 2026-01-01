import React from 'react';

export default function SearchFilter({
    keyword, setKeyword,
    jobTypeFilter, setJobTypeFilter,
}) {
    return (
        <div className="search-bar mx-auto flex items-center gap-2 mt-8 max-w-2xl">
            {/* Small, properly sized search icon */}
            <div className="flex items-center justify-center pl-4 pr-2">
                <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor" 
                    className="w-5 h-5 text-gray-500"
                >
                    <path 
                        strokeLinecap="round" 
                        strokeLinejoin="round" 
                        strokeWidth={2} 
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" 
                    />
                </svg>
            </div>
            
            <input
                type="text"
                placeholder="Search jobs, companies, or skills..."
                value={keyword}
                onChange={e => setKeyword(e.target.value)}
                className="flex-grow py-3 px-2"
            />
            
            <select
                value={jobTypeFilter}
                onChange={e => setJobTypeFilter(e.target.value)}
                className="mr-2"
            >
                <option value="On-site KSA">On-site KSA</option>
                <option value="Remote">Remote</option>
            </select>
            
            <button type="button">
                Search
            </button>
        </div>
    );
}
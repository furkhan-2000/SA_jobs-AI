import React from 'react';

export default function SearchFilter({
    keyword, setKeyword,
    jobTypeFilter, setJobTypeFilter,
}) {
    return (
        <div className="search-bar glass-ui mx-auto flex items-center gap-2 mt-8 rounded-full p-1 max-w-2xl shadow-lg transition-all duration-300 ease-in-out hover:shadow-xl">
            {/* Smaller, inline search icon */}
            <div className="search-icon flex items-center h-full pl-4 text-gray-600">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="m21 21-3.5-3.5M10 17a7 7 0 1 0 0-14 7 7 0 0 0 0 14Z" />
                </svg>
            </div>
            <input
                type="text"
                placeholder="Search jobs, companies, or skills..."
                value={keyword}
                onChange={e => setKeyword(e.target.value)}
                className="flex-grow border-none outline-none bg-transparent text-gray-800 text-sm py-2 px-2 placeholder-gray-500"
            />
            <select
                value={jobTypeFilter}
                onChange={e => setJobTypeFilter(e.target.value)}
                className="glass-ui appearance-none bg-transparent border-none text-gray-800 py-2 px-3 rounded-full cursor-pointer focus:outline-none focus:ring-2 focus:ring-white/50 text-xs font-semibold"
            >
                <option value="On-site KSA">On-site KSA</option>
                <option value="Remote">Remote</option>
            </select>
            <button
                className="cta-button font-semibold text-sm py-2 px-6 rounded-full bg-gray-800 text-white shadow-md hover:bg-gray-700 transition-colors duration-200"
            >
                Search
            </button>
        </div>
    );
}
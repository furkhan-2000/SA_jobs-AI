import React from 'react';

export default function SearchFilter({
    keyword, setKeyword,
    jobTypeFilter, setJobTypeFilter,
}) {
    return (
        <div className="search-bar glass-ui mx-auto flex items-center gap-2 mt-8 rounded-full p-1 max-w-2xl shadow-lg transition-all duration-300 ease-in-out hover:shadow-xl">
            <div className="search-icon flex items-center h-full pl-3 text-gray-700">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-3.5-3.5M10 17a7 7 0 1 0 0-14 7 7 0 0 0 0 14Z" />
                </svg>
            </div>
            <input
                type="text"
                placeholder="Search jobs, companies, or skills..."
                value={keyword}
                onChange={e => setKeyword(e.target.value)}
                className="flex-grow border-none outline-none bg-transparent text-gray-800 text-base py-2 px-2"
            />
            <select
                value={jobTypeFilter}
                onChange={e => setJobTypeFilter(e.target.value)}
                className="glass-ui appearance-none bg-transparent border-none text-gray-800 py-2 px-3 rounded-full cursor-pointer focus:outline-none focus:ring-2 focus:ring-white/50 text-sm font-semibold"
            >
                <option value="On-site KSA">On-site KSA</option>
                <option value="Remote">Remote</option>
            </select>
            <button
                // onClick={onSearch} // onSearch is no longer a prop or needed here directly due to debouncing
                className="cta-button font-bold py-2 px-5 rounded-full bg-gray-800 text-white shadow-md hover:bg-gray-700 transition-colors duration-200 hover:scale-105 hover:shadow-xl" // Enhanced hover
            >
                Search
            </button>
        </div>
    );
}
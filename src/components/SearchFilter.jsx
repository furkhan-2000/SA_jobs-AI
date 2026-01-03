import React from 'react';

export default function SearchFilter({
    keyword, setKeyword,
    jobTypeFilter, setJobTypeFilter,
}) {
    return (
        <div className="search-bar mx-auto flex items-center gap-2 mt-8 max-w-2xl">
            <input
                type="text"
                placeholder="Search jobs, companies, or skills..."
                value={keyword}
                onChange={e => setKeyword(e.target.value)}
                className="flex-grow py-3 px-4"
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
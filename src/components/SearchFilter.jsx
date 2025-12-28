import React from 'react';

export default function SearchFilter({
    keyword, setKeyword,
    jobTypeFilter, setJobTypeFilter,
}) {
    return (
        <div className="search-filter">
            <input
                type="text"
                placeholder="Search by keyword..."
                value={keyword}
                onChange={e => setKeyword(e.target.value)}
            />
            <select value={jobTypeFilter} onChange={e => setJobTypeFilter(e.target.value)}>
                <option value="On-site KSA">On-site KSA</option>
                <option value="Remote">Remote</option>
            </select>
        </div>
    );
}

import React from 'react';

export default function SearchFilter({
    keyword, setKeyword,
    jobTypeFilter, setJobTypeFilter,
    locationFilter, setLocationFilter,
    jobTypes = [], // Default to empty array
    locations = [], // Default to empty array
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
                <option value="">All Job Types</option>
                {jobTypes.map((type, index) => (
                    <option key={`${type}-${index}`} value={type}>{type}</option>
                ))}
            </select>
            <select value={locationFilter} onChange={e => setLocationFilter(e.target.value)}>
                <option value="">All Locations</option>
                {locations.map((location, index) => (
                    <option key={`${location}-${index}`} value={location}>{location}</option>
                ))}
            </select>
        </div>
    );
}

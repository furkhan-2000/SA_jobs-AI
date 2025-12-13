import React, { useState } from "react";

export default function SearchFilter({ keyword, setKeyword, jobType, setJobType, industry, setIndustry, onSearch }) {
    return (
        <div className="search-filter">
            <input
                type="text"
                placeholder="Search jobs..."
                value={keyword}
                onChange={e => setKeyword(e.target.value)}
            />
            <input
                type="text"
                placeholder="Job type..."
                value={jobType}
                onChange={e => setJobType(e.target.value)}
            />
            <input
                type="text"
                placeholder="Industry..."
                value={industry}
                onChange={e => setIndustry(e.target.value)}
            />
            <button onClick={onSearch}>Search</button>
        </div>
    );
}

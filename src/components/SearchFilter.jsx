import React, { useState } from "react";

export default function SearchFilter({ keyword, setKeyword, onSearch }) {
    return (
        <div className="search-filter">
            <input
                type="text"
                placeholder="Search jobs..."
                value={keyword}
                onChange={e => setKeyword(e.target.value)}
            />
            <button onClick={onSearch}>Search</button>
        </div>
    );
}

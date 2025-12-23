import React from 'react';

export default function SkeletonJobCard() {
    return (
        <div className="job-card skeleton">
            <div className="skeleton-line skeleton-title"></div>
            <div className="skeleton-line skeleton-company"></div>
            <div className="skeleton-line skeleton-location"></div>
            <div className="skeleton-line skeleton-button"></div>
        </div>
    );
}

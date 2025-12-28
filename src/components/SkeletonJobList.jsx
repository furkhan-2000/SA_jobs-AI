import React from 'react';
import SkeletonJobCard from './SkeletonJobCard';

export default function SkeletonJobList({ count = 5 }) {
    return (
        <div className="job-list">
            {Array.from({ length: count }).map((_, index) => (
                <SkeletonJobCard key={index} /> // OK to use index as key for static placeholder list
            ))}
        </div>
    );
}

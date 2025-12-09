import React from "react";
import { FixedSizeList as List } from "react-window";
import JobCard from "./JobCard";

export default function JobList({ jobs }) {
    const Row = ({ index, style }) => (
        <div style={style}>
            <JobCard job={jobs[index]} />
        </div>
    );

    return (
        <List
            height={600}
            itemCount={jobs.length}
            itemSize={120}
            width={"100%"}
        >
            {Row}
        </List>
    );
}

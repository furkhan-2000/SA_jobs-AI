import { JobCard } from "./JobCard.js";

export function JobList(jobs) {
    return `
        <div>
            ${jobs.map(job => JobCard(job)).join("")}
        </div>
    `;
}

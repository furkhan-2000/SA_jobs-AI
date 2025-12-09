export function JobCard(job) {
    return `
        <div class="job-card">
            <div class="job-title">${job.title}</div>
            <div class="job-company">${job.company || "Unknown Company"}</div>
            <div>${job.location || "Location not provided"}</div>
            <a href="${job.url}" target="_blank">View Job</a>
        </div>
    `;
}

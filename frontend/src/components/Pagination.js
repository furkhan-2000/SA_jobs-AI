export function Pagination(currentPage, totalPages) {
    return `
        <div class="pagination">
            <button ${currentPage === 1 ? "disabled" : ""} data-action="prev">Prev</button>
            <span>${currentPage} / ${totalPages}</span>
            <button ${currentPage === totalPages ? "disabled" : ""} data-action="next">Next</button>
        </div>
    `;
}

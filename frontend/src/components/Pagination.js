import React from "react";

export default function Pagination({ page, setPage, total, pageSize }) {
    const totalPages = Math.ceil(total / pageSize);

    const prev = () => setPage(p => Math.max(1, p - 1));
    const next = () => setPage(p => Math.min(totalPages, p + 1));

    return (
        <div className="pagination">
            <button onClick={prev} disabled={page === 1}>Prev</button>
            <span>{page} / {totalPages}</span>
            <button onClick={next} disabled={page === totalPages}>Next</button>
        </div>
    );
}

import React from "react";

function Pagination({ page, total, pageSize, setPage }) {
  const totalPages = Math.ceil(total / pageSize);

  const prevPage = () => {
    if (page > 1) setPage(page - 1);
  };

  const nextPage = () => {
    if (page < totalPages) setPage(page + 1);
  };

  return (
    <div className="pagination flex justify-between items-center">
      <button
        onClick={prevPage}
        disabled={page === 1}
        className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
      >
        Previous
      </button>

      <span>
        Page {page} of {totalPages}
      </span>

      <button
        onClick={nextPage}
        disabled={page === totalPages}
        className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
      >
        Next
      </button>
    </div>
  );
}

export default Pagination;

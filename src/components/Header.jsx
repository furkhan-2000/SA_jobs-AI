import React from "react";

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 p-4">
      <nav className="nav glass-ui mx-auto flex justify-between items-center px-6 py-3 rounded-full max-w-4xl">
        <div className="logo flex items-center font-bold text-xl text-gray-800 gap-2 cursor-pointer" onClick={() => window.location.reload()}>
          <span>🇸🇦</span> WazifHub
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={() => console.log("Language toggle")}
            className="font-medium text-sm px-4 py-2 rounded-full border border-white/20 text-gray-800 bg-white/10 transition-all duration-300 ease-in-out hover:bg-white/25"
          >
            عربي
          </button>
        </div>
      </nav>
    </header>
  );
}
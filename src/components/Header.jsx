import React from "react";

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 p-4">
      <nav className="nav mx-auto flex justify-between items-center px-6 py-3 max-w-4xl">
        <div 
          className="flex items-center font-bold text-xl text-gray-800 gap-2 cursor-pointer" 
          onClick={() => window.location.reload()}
        >
          <span>🇸🇦</span>
          <span>WazifHub</span>
        </div>
        
        <button
          onClick={() => console.log("Language toggle")}
          className="font-medium text-sm px-4 py-2 rounded-full border border-gray-300 text-gray-800 bg-white hover:bg-gray-50 transition-all duration-200"
        >
          عربي
        </button>
      </nav>
    </header>
  );
}
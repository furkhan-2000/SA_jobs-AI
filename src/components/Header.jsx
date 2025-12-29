import React from "react";

export default function Header() {
  const isArabic = false;

  const handleLanguageToggle = () => {
    console.log("Language toggle clicked");
  };

  const handleLoginClick = () => {
    console.log("Login clicked");
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 p-4">
      <nav className="nav glass-ui mx-auto flex justify-between items-center px-4 py-2 rounded-full max-w-4xl">
        <div className="logo flex items-center font-bold text-lg text-gray-800 gap-2 cursor-pointer" onClick={() => window.location.reload()}>
          WazifHub
        </div>
        <div>
          <button
            onClick={handleLanguageToggle}
            className="font-semibold px-3 py-1 rounded-lg border border-white/15 text-gray-800 bg-white/15 transition-all duration-300 ease-in-out hover:bg-white/30 hover:scale-105 hover:shadow-lg" // Enhanced hover
          >
            {isArabic ? 'English' : 'عربي'}
          </button>
          <span
            className="ml-3 font-bold cursor-pointer text-gray-800 transition-all duration-300 ease-in-out hover:text-gray-900 hover:scale-105" // Enhanced hover for login text
            onClick={handleLoginClick}
          >
            Login
          </span>
        </div>
      </nav>
    </header>
  );
}
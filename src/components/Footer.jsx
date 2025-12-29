import React from "react";

export default function Footer() {
    return (
        <footer className="footer glass-ui p-4 text-center text-gray-700 mt-8 rounded-t-xl">
            <p className="text-sm">
                Designed & Developed by <a href="https://www.linkedin.com/in/khan-mohammed-790b18214" target="_blank" rel="noopener noreferrer" className="font-semibold text-gray-800 hover:underline">Khan Mohammed</a>
                <br/>
                © {new Date().getFullYear()} WazifHub | Proudly Supporting Vision 2030
            </p>
        </footer>
    );
}
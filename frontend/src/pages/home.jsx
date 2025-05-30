// src/pages/home.jsx

import React from "react";
import { Link } from "react-router-dom"; // ✅ Link 추가

export default function Home() {
    return (
        <div className="min-h-screen bg-white text-gray-900 font-sans">

            {/* Hero Section */}
            <main className="flex flex-col items-center justify-center text-center px-4 py-24">
                <h1 className="text-4xl md:text-6xl font-bold mb-6">
                    Discover Your Strengths with AI
                </h1>
                <p className="text-lg md:text-xl text-gray-600 max-w-xl mb-8">
                    Narulab analyzes your personality and aptitude to help you find the best-fit career path. All powered by STEN, GPT, and smart diagnostics.
                </p>
                <a
                    href="/signup"
                    className="bg-blue-500 text-white px-6 py-3 rounded-full text-lg font-semibold hover:bg-blue-600"
                >
                    Start Your Test
                </a>
            </main>

            {/* Footer */}
            <footer className="border-t border-gray-200 px-8 py-6 text-sm text-gray-500 text-center">
                © 2025 Narulab. All rights reserved. · <a href="#terms" className="hover:text-gray-700">Terms</a> · <a href="mailto:support@narulab.com" className="hover:text-gray-700">support@narulab.com</a>
            </footer>
        </div>
    );
}

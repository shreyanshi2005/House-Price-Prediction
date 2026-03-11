import { useState } from "react";
import {
    Home,
    Github,
    Sun,
    Moon,
    BrainCircuit,
} from "lucide-react";

export default function Navbar({ darkMode, setDarkMode }) {
    return (
        <nav className="sticky top-0 z-50 border-b border-white/10">
            <div
                className={`${darkMode
                        ? "bg-surface-900/80 backdrop-blur-xl"
                        : "bg-white/80 backdrop-blur-xl border-b border-surface-200"
                    } transition-colors duration-300`}
            >
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        {/* Logo + Title */}
                        <div className="flex items-center gap-3">
                            <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 shadow-lg">
                                <BrainCircuit className="w-5 h-5 text-white" />
                            </div>
                            <div>
                                <h1
                                    className={`text-lg font-bold leading-tight ${darkMode ? "text-white" : "text-surface-900"
                                        }`}
                                >
                                    House Price Prediction
                                </h1>
                                <p
                                    className={`text-xs leading-tight ${darkMode ? "text-surface-200/60" : "text-surface-700/60"
                                        }`}
                                >
                                    ML-Powered Real Estate Estimator
                                </p>
                            </div>
                        </div>

                        {/* Right side */}
                        <div className="flex items-center gap-2">
                            {/* GitHub */}
                            <a
                                href="https://github.com/shreyanshi2005"
                                target="_blank"
                                rel="noopener noreferrer"
                                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${darkMode
                                        ? "text-surface-200/70 hover:text-white hover:bg-white/10"
                                        : "text-surface-700 hover:text-surface-900 hover:bg-surface-100"
                                    }`}
                            >
                                <Github className="w-4 h-4" />
                                <span className="hidden sm:inline">GitHub</span>
                            </a>

                            {/* Dark mode toggle */}
                            <button
                                onClick={() => setDarkMode(!darkMode)}
                                className={`p-2 rounded-lg transition-all duration-300 ${darkMode
                                        ? "text-amber-400 hover:bg-white/10"
                                        : "text-primary-600 hover:bg-primary-50"
                                    }`}
                                aria-label="Toggle theme"
                            >
                                {darkMode ? (
                                    <Sun className="w-5 h-5" />
                                ) : (
                                    <Moon className="w-5 h-5" />
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
}

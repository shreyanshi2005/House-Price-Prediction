import { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem("hpp_darkMode");
    return saved !== null ? JSON.parse(saved) : true; // default dark
  });

  useEffect(() => {
    localStorage.setItem("hpp_darkMode", JSON.stringify(darkMode));
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode
        ? "bg-surface-950 text-white"
        : "bg-gradient-to-br from-surface-50 via-primary-50/20 to-surface-50 text-surface-900"
      }`}>
      <Navbar darkMode={darkMode} setDarkMode={setDarkMode} />
      <Dashboard darkMode={darkMode} />
    </div>
  );
}

export default App;

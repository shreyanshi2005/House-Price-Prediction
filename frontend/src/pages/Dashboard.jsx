import { useState, useCallback } from "react";
import PredictionForm from "../components/PredictionForm";
import ResultCard from "../components/ResultCard";
import FeatureChart from "../components/FeatureChart";
import ModelInfoPanel from "../components/ModelInfoPanel";
import HistoryTable from "../components/HistoryTable";
import { predictPrice } from "../services/api";

const HISTORY_KEY = "hpp_prediction_history";

function loadHistory() {
    try {
        return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
    } catch {
        return [];
    }
}

export default function Dashboard({ darkMode }) {
    const [prediction, setPrediction] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [history, setHistory] = useState(loadHistory);

    const handlePredict = useCallback(async (formData) => {
        setIsLoading(true);
        setError(null);
        setPrediction(null);

        try {
            const result = await predictPrice(formData);
            setPrediction(result);

            // Store in history
            const entry = {
                ...formData,
                predicted_price: result.predicted_price,
                timestamp: Date.now(),
            };
            const newHistory = [entry, ...history].slice(0, 10);
            setHistory(newHistory);
            localStorage.setItem(HISTORY_KEY, JSON.stringify(newHistory));
        } catch (err) {
            const msg =
                err.response?.data?.detail ||
                err.message ||
                "Failed to connect to the prediction API. Make sure the backend is running.";
            setError(msg);
        } finally {
            setIsLoading(false);
        }
    }, [history]);

    const clearHistory = () => {
        setHistory([]);
        localStorage.removeItem(HISTORY_KEY);
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Hero section */}
            <div className="text-center mb-10">
                <h2 className={`text-3xl sm:text-4xl font-bold mb-3 ${darkMode ? "text-white" : "text-surface-900"
                    }`}>
                    Predict House{" "}
                    <span className="bg-gradient-to-r from-primary-500 to-accent-500 bg-clip-text text-transparent">
                        Prices
                    </span>
                </h2>
                <p className={`max-w-xl mx-auto ${darkMode ? "text-surface-200/50" : "text-surface-700/60"
                    }`}>
                    Enter property details below to get an instant ML-powered price estimation
                    using our trained Gradient Boosting model.
                </p>
            </div>

            {/* Main grid — Form + Result */}
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-6">
                <div className="lg:col-span-3">
                    <PredictionForm
                        onPredict={handlePredict}
                        isLoading={isLoading}
                        darkMode={darkMode}
                    />
                </div>
                <div className="lg:col-span-2 flex flex-col gap-6">
                    <ResultCard
                        prediction={prediction}
                        isLoading={isLoading}
                        error={error}
                        darkMode={darkMode}
                    />
                </div>
            </div>

            {/* Charts + Model info */}
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-6">
                <div className="lg:col-span-3">
                    <FeatureChart darkMode={darkMode} />
                </div>
                <div className="lg:col-span-2">
                    <ModelInfoPanel darkMode={darkMode} />
                </div>
            </div>

            {/* History */}
            <HistoryTable
                history={history}
                onClear={clearHistory}
                darkMode={darkMode}
            />

            {/* Footer */}
            <footer className={`text-center mt-12 pb-6 text-xs ${darkMode ? "text-surface-200/30" : "text-surface-700/30"
                }`}>
                Built with React, Tailwind CSS & FastAPI · Powered by scikit-learn
            </footer>
        </div>
    );
}

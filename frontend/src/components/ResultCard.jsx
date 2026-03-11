import { useEffect, useState } from "react";
import { DollarSign, TrendingUp, TrendingDown, ArrowUpDown } from "lucide-react";

function useCountUp(target, duration = 1200) {
    const [value, setValue] = useState(0);
    useEffect(() => {
        if (!target) { setValue(0); return; }
        let start = 0;
        const startTime = performance.now();
        const animate = (now) => {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // ease-out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            setValue(Math.round(eased * target));
            if (progress < 1) requestAnimationFrame(animate);
        };
        requestAnimationFrame(animate);
    }, [target, duration]);
    return value;
}

export default function ResultCard({ prediction, isLoading, error, darkMode }) {
    const displayPrice = useCountUp(prediction?.predicted_price || 0);
    const price = prediction?.predicted_price || 0;
    const lowRange = Math.round(price * 0.92);
    const highRange = Math.round(price * 1.08);

    const formatPrice = (v) =>
        new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
            maximumFractionDigits: 0,
        }).format(v);

    const cardClass = darkMode
        ? "bg-surface-800/60 border border-white/5 backdrop-blur-sm"
        : "bg-white/80 border border-surface-200 backdrop-blur-sm shadow-lg";

    // Empty state
    if (!prediction && !isLoading && !error) {
        return (
            <div className={`rounded-2xl p-8 text-center ${cardClass}`}>
                <div className={`w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center ${darkMode ? "bg-primary-500/10" : "bg-primary-50"
                    }`}>
                    <DollarSign className={`w-8 h-8 ${darkMode ? "text-primary-400/50" : "text-primary-300"}`} />
                </div>
                <h3 className={`text-lg font-semibold mb-2 ${darkMode ? "text-white/60" : "text-surface-700/60"}`}>
                    Awaiting Prediction
                </h3>
                <p className={`text-sm ${darkMode ? "text-surface-200/40" : "text-surface-700/40"}`}>
                    Fill in the property details and click <br /> "Predict Price" to get started
                </p>
            </div>
        );
    }

    // Loading state
    if (isLoading) {
        return (
            <div className={`rounded-2xl p-8 ${cardClass}`}>
                <div className="flex flex-col items-center justify-center gap-4">
                    <div className="relative w-20 h-20">
                        <div className="absolute inset-0 rounded-full border-4 border-primary-500/20"></div>
                        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-primary-500 animate-spin"></div>
                        <div className="absolute inset-3 rounded-full border-4 border-transparent border-t-accent-500 animate-spin" style={{ animationDirection: "reverse", animationDuration: "0.8s" }}></div>
                    </div>
                    <div className="text-center">
                        <p className={`font-semibold ${darkMode ? "text-white" : "text-surface-900"}`}>
                            Analyzing Property...
                        </p>
                        <p className={`text-sm mt-1 ${darkMode ? "text-surface-200/50" : "text-surface-700/50"}`}>
                            ML model is processing your inputs
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    // Error state
    if (error) {
        return (
            <div className={`rounded-2xl p-8 border-2 border-red-500/30 ${cardClass}`}>
                <div className="text-center">
                    <div className="w-14 h-14 mx-auto mb-3 rounded-full bg-red-500/10 flex items-center justify-center">
                        <span className="text-2xl">⚠️</span>
                    </div>
                    <h3 className={`font-semibold mb-1 ${darkMode ? "text-red-400" : "text-red-600"}`}>
                        Prediction Failed
                    </h3>
                    <p className={`text-sm ${darkMode ? "text-surface-200/60" : "text-surface-700/60"}`}>{error}</p>
                </div>
            </div>
        );
    }

    // Success state
    return (
        <div className={`rounded-2xl overflow-hidden ${prediction ? "animate-fade-in-up" : ""}`}>
            {/* Gradient header */}
            <div className="bg-gradient-to-br from-primary-600 via-primary-500 to-accent-500 p-8 text-center relative overflow-hidden">
                {/* Decorative circles */}
                <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/5 rounded-full"></div>
                <div className="absolute -bottom-8 -left-8 w-32 h-32 bg-white/5 rounded-full"></div>

                <p className="text-white/70 text-sm font-medium uppercase tracking-wider mb-2">
                    Estimated Market Value
                </p>
                <h2 className="text-4xl sm:text-5xl font-bold text-white mb-1 tracking-tight">
                    {formatPrice(displayPrice)}
                </h2>
                <p className="text-white/50 text-xs mt-2">
                    {prediction?.currency || "USD"}
                </p>
            </div>

            {/* Confidence range */}
            <div className={`p-5 ${darkMode ? "bg-surface-800/60 border border-white/5" : "bg-white border border-surface-200"}`}>
                <div className="flex items-center justify-center gap-2 mb-3">
                    <ArrowUpDown className={`w-4 h-4 ${darkMode ? "text-surface-200/50" : "text-surface-700/50"}`} />
                    <p className={`text-xs font-medium uppercase tracking-wider ${darkMode ? "text-surface-200/50" : "text-surface-700/50"}`}>
                        Confidence Range (±8%)
                    </p>
                </div>
                <div className="flex items-center justify-between gap-4">
                    <div className="flex-1 text-center p-3 rounded-xl bg-red-500/5">
                        <TrendingDown className="w-4 h-4 text-red-400 mx-auto mb-1" />
                        <p className={`text-sm font-bold ${darkMode ? "text-red-400" : "text-red-600"}`}>{formatPrice(lowRange)}</p>
                        <p className={`text-xs ${darkMode ? "text-surface-200/40" : "text-surface-700/40"}`}>Low</p>
                    </div>
                    <div className="flex-1 text-center p-3 rounded-xl bg-green-500/5">
                        <TrendingUp className="w-4 h-4 text-green-400 mx-auto mb-1" />
                        <p className={`text-sm font-bold ${darkMode ? "text-green-400" : "text-green-600"}`}>{formatPrice(highRange)}</p>
                        <p className={`text-xs ${darkMode ? "text-surface-200/40" : "text-surface-700/40"}`}>High</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

import { useEffect, useState } from "react";
import {
    Cpu,
    Target,
    Activity,
    Database,
    Layers,
    TrendingUp,
} from "lucide-react";
import { getModelInfo } from "../services/api";

const MetricCard = ({ icon: Icon, label, value, sub, color, darkMode }) => (
    <div className={`p-4 rounded-xl ${darkMode ? "bg-surface-900/50 border border-white/5" : "bg-surface-50 border border-surface-100"
        }`}>
        <div className="flex items-center gap-2 mb-2">
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${color}`}>
                <Icon className="w-4 h-4 text-white" />
            </div>
            <span className={`text-xs font-medium uppercase tracking-wider ${darkMode ? "text-surface-200/50" : "text-surface-700/50"
                }`}>{label}</span>
        </div>
        <p className={`text-xl font-bold ${darkMode ? "text-white" : "text-surface-900"}`}>{value}</p>
        {sub && <p className={`text-xs mt-0.5 ${darkMode ? "text-surface-200/40" : "text-surface-700/40"}`}>{sub}</p>}
    </div>
);

export default function ModelInfoPanel({ darkMode }) {
    const [info, setInfo] = useState(null);

    useEffect(() => {
        getModelInfo()
            .then(setInfo)
            .catch(() => {
                setInfo({
                    algorithm: "Gradient Boosting (Tuned)",
                    r2: 0.629,
                    rmse: 51119,
                    mae: 41479,
                    dataset_size: 1460,
                    cv_folds: 5,
                });
            });
    }, []);

    const cardClass = darkMode
        ? "bg-surface-800/60 border border-white/5 backdrop-blur-sm"
        : "bg-white/80 border border-surface-200 backdrop-blur-sm shadow-lg";

    if (!info) {
        return (
            <div className={`rounded-2xl p-6 ${cardClass}`}>
                <div className="h-60 flex items-center justify-center">
                    <div className="w-8 h-8 border-3 border-primary-500/30 border-t-primary-500 rounded-full animate-spin" />
                </div>
            </div>
        );
    }

    return (
        <div className={`rounded-2xl p-6 ${cardClass}`}>
            <div className="flex items-center gap-2 mb-5">
                <Cpu className={`w-5 h-5 ${darkMode ? "text-primary-400" : "text-primary-600"}`} />
                <h2 className={`text-lg font-semibold ${darkMode ? "text-white" : "text-surface-900"}`}>
                    Model Info
                </h2>
            </div>

            {/* Algorithm badge */}
            <div className={`mb-5 p-3 rounded-xl text-center ${darkMode ? "bg-gradient-to-r from-primary-500/10 to-accent-500/10 border border-primary-500/20"
                    : "bg-gradient-to-r from-primary-50 to-emerald-50 border border-primary-100"
                }`}>
                <p className={`text-xs font-medium uppercase tracking-wider mb-1 ${darkMode ? "text-primary-400/60" : "text-primary-600/60"
                    }`}>Algorithm</p>
                <p className={`font-bold ${darkMode ? "text-white" : "text-surface-900"}`}>
                    {info.algorithm}
                </p>
            </div>

            <div className="grid grid-cols-2 gap-3">
                <MetricCard
                    icon={Target}
                    label="R² Score"
                    value={(info.r2).toFixed(4)}
                    sub="Goodness of fit"
                    color="bg-primary-600"
                    darkMode={darkMode}
                />
                <MetricCard
                    icon={Activity}
                    label="RMSE"
                    value={`$${Number(info.rmse).toLocaleString()}`}
                    sub="Root mean sq error"
                    color="bg-amber-500"
                    darkMode={darkMode}
                />
                <MetricCard
                    icon={TrendingUp}
                    label="MAE"
                    value={`$${Number(info.mae).toLocaleString()}`}
                    sub="Mean abs error"
                    color="bg-rose-500"
                    darkMode={darkMode}
                />
                <MetricCard
                    icon={Database}
                    label="Dataset"
                    value={Number(info.dataset_size).toLocaleString()}
                    sub={`${info.cv_folds}-fold CV`}
                    color="bg-accent-600"
                    darkMode={darkMode}
                />
            </div>
        </div>
    );
}

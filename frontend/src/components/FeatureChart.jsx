import { useEffect, useState } from "react";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Cell,
} from "recharts";
import { BarChart3 } from "lucide-react";
import { getFeatureImportance } from "../services/api";

const GRADIENT_COLORS = [
    "#6366f1", "#7c7ff7", "#818cf8", "#8b8ff9",
    "#a5b4fc", "#b4bcfc", "#c7d2fe", "#d4daff",
    "#e0e7ff", "#eef2ff",
];

export default function FeatureChart({ darkMode }) {
    const [features, setFeatures] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getFeatureImportance()
            .then((data) => setFeatures(data.features || []))
            .catch(() => {
                // Fallback data if API is down
                setFeatures([
                    { name: "Overall Quality", importance: 0.312 },
                    { name: "Living Area", importance: 0.189 },
                    { name: "Basement SF", importance: 0.098 },
                    { name: "Garage Cars", importance: 0.082 },
                    { name: "Year Built", importance: 0.075 },
                    { name: "Bathrooms", importance: 0.058 },
                    { name: "Lot Area", importance: 0.045 },
                    { name: "Kitchen Qual", importance: 0.039 },
                    { name: "Fireplaces", importance: 0.032 },
                    { name: "Garage Area", importance: 0.028 },
                ]);
            })
            .finally(() => setLoading(false));
    }, []);

    const cardClass = darkMode
        ? "bg-surface-800/60 border border-white/5 backdrop-blur-sm"
        : "bg-white/80 border border-surface-200 backdrop-blur-sm shadow-lg";

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className={`px-3 py-2 rounded-lg text-sm ${darkMode ? "bg-surface-900 border border-white/10 text-white" : "bg-white border border-surface-200 text-surface-900 shadow-lg"
                    }`}>
                    <p className="font-medium">{payload[0].payload.name}</p>
                    <p className={darkMode ? "text-primary-400" : "text-primary-600"}>
                        {(payload[0].value * 100).toFixed(1)}% importance
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className={`rounded-2xl p-6 ${cardClass}`}>
            <div className="flex items-center gap-2 mb-5">
                <BarChart3 className={`w-5 h-5 ${darkMode ? "text-primary-400" : "text-primary-600"}`} />
                <h2 className={`text-lg font-semibold ${darkMode ? "text-white" : "text-surface-900"}`}>
                    Feature Impact
                </h2>
                <span className={`text-xs px-2 py-0.5 rounded-full ml-auto ${darkMode ? "bg-primary-500/10 text-primary-400" : "bg-primary-50 text-primary-600"
                    }`}>SHAP</span>
            </div>

            {loading ? (
                <div className="h-64 flex items-center justify-center">
                    <div className="w-8 h-8 border-3 border-primary-500/30 border-t-primary-500 rounded-full animate-spin" />
                </div>
            ) : (
                <ResponsiveContainer width="100%" height={320}>
                    <BarChart data={features} layout="vertical" margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
                        <CartesianGrid
                            strokeDasharray="3 3"
                            stroke={darkMode ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.06)"}
                            horizontal={false}
                        />
                        <XAxis
                            type="number"
                            tick={{ fill: darkMode ? "#94a3b8" : "#64748b", fontSize: 11 }}
                            axisLine={false}
                            tickLine={false}
                            tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                        />
                        <YAxis
                            type="category"
                            dataKey="name"
                            width={110}
                            tick={{ fill: darkMode ? "#cbd5e1" : "#475569", fontSize: 12 }}
                            axisLine={false}
                            tickLine={false}
                        />
                        <Tooltip content={<CustomTooltip />} cursor={false} />
                        <Bar dataKey="importance" radius={[0, 6, 6, 0]} barSize={22}>
                            {features.map((_, idx) => (
                                <Cell key={idx} fill={GRADIENT_COLORS[idx] || GRADIENT_COLORS[0]} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}

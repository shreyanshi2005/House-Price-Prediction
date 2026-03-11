import { History, Trash2 } from "lucide-react";

export default function HistoryTable({ history, onClear, darkMode }) {
    const cardClass = darkMode
        ? "bg-surface-800/60 border border-white/5 backdrop-blur-sm"
        : "bg-white/80 border border-surface-200 backdrop-blur-sm shadow-lg";

    const formatPrice = (v) =>
        new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
            maximumFractionDigits: 0,
        }).format(v);

    return (
        <div className={`rounded-2xl p-6 ${cardClass}`}>
            <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-2">
                    <History className={`w-5 h-5 ${darkMode ? "text-primary-400" : "text-primary-600"}`} />
                    <h2 className={`text-lg font-semibold ${darkMode ? "text-white" : "text-surface-900"}`}>
                        Prediction History
                    </h2>
                    {history.length > 0 && (
                        <span className={`text-xs px-2 py-0.5 rounded-full ${darkMode ? "bg-primary-500/10 text-primary-400" : "bg-primary-50 text-primary-600"
                            }`}>
                            {history.length}
                        </span>
                    )}
                </div>
                {history.length > 0 && (
                    <button
                        onClick={onClear}
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${darkMode
                                ? "text-red-400/70 hover:bg-red-500/10 hover:text-red-400"
                                : "text-red-500/70 hover:bg-red-50 hover:text-red-600"
                            }`}
                    >
                        <Trash2 className="w-3.5 h-3.5" /> Clear
                    </button>
                )}
            </div>

            {history.length === 0 ? (
                <div className={`text-center py-8 ${darkMode ? "text-surface-200/30" : "text-surface-700/30"}`}>
                    <History className="w-10 h-10 mx-auto mb-2 opacity-30" />
                    <p className="text-sm">No predictions yet</p>
                </div>
            ) : (
                <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                        <thead>
                            <tr className={`border-b ${darkMode ? "border-white/10" : "border-surface-200"}`}>
                                {["#", "Neighborhood", "Area", "Beds", "Quality", "Price"].map((h) => (
                                    <th key={h} className={`text-left py-2.5 px-3 text-xs font-semibold uppercase tracking-wider ${darkMode ? "text-surface-200/40" : "text-surface-700/40"
                                        }`}>{h}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((item, idx) => (
                                <tr
                                    key={idx}
                                    className={`border-b last:border-b-0 transition-colors ${darkMode
                                            ? "border-white/5 hover:bg-white/3"
                                            : "border-surface-100 hover:bg-surface-50"
                                        }`}
                                >
                                    <td className={`py-3 px-3 ${darkMode ? "text-surface-200/40" : "text-surface-700/40"}`}>
                                        {history.length - idx}
                                    </td>
                                    <td className={`py-3 px-3 font-medium ${darkMode ? "text-white" : "text-surface-900"}`}>
                                        {item.Neighborhood}
                                    </td>
                                    <td className={`py-3 px-3 ${darkMode ? "text-surface-200/70" : "text-surface-700"}`}>
                                        {Number(item.GrLivArea).toLocaleString()} ft²
                                    </td>
                                    <td className={`py-3 px-3 ${darkMode ? "text-surface-200/70" : "text-surface-700"}`}>
                                        {item.BedroomAbvGr}
                                    </td>
                                    <td className="py-3 px-3">
                                        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${item.OverallQual >= 7
                                                ? darkMode ? "bg-green-500/10 text-green-400" : "bg-green-50 text-green-700"
                                                : item.OverallQual >= 5
                                                    ? darkMode ? "bg-amber-500/10 text-amber-400" : "bg-amber-50 text-amber-700"
                                                    : darkMode ? "bg-red-500/10 text-red-400" : "bg-red-50 text-red-700"
                                            }`}>
                                            {item.OverallQual}/10
                                        </span>
                                    </td>
                                    <td className={`py-3 px-3 font-semibold ${darkMode ? "text-accent-400" : "text-accent-600"}`}>
                                        {formatPrice(item.predicted_price)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

import { useState } from "react";
import {
    Home,
    Ruler,
    BedDouble,
    Bath,
    Car,
    Calendar,
    MapPin,
    ChefHat,
    LandPlot,
    Warehouse,
    Sparkles,
    Loader2,
    Star,
} from "lucide-react";

const NEIGHBORHOODS = [
    "NAmes", "CollgCr", "OldTown", "Edwards", "Somerst",
    "NridgHt", "Gilbert", "Sawyer", "NWAmes", "SawyerW",
    "BrkSide", "Crawfor", "Mitchel", "NoRidge", "Timber",
    "IDOTRR", "StoneBr", "ClearCr", "SWISU", "Blmngtn",
    "MeadowV", "BrDale", "Veenker", "NPkVill", "Blueste",
];

const KITCHEN_QUALITY = [
    { value: "Ex", label: "Excellent" },
    { value: "Gd", label: "Good" },
    { value: "TA", label: "Average" },
    { value: "Fa", label: "Fair" },
    { value: "Po", label: "Poor" },
];

const INITIAL_FORM = {
    OverallQual: 7,
    GrLivArea: 1500,
    YearBuilt: 2005,
    BedroomAbvGr: 3,
    FullBath: 2,
    GarageCars: 2,
    LotArea: 8500,
    TotalBsmtSF: 850,
    Neighborhood: "CollgCr",
    KitchenQual: "Gd",
};

export default function PredictionForm({ onPredict, isLoading, darkMode }) {
    const [form, setForm] = useState(INITIAL_FORM);

    const update = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

    const handleSubmit = (e) => {
        e.preventDefault();
        onPredict(form);
    };

    const cardClass = darkMode
        ? "bg-surface-800/60 border border-white/5 backdrop-blur-sm"
        : "bg-white/80 border border-surface-200 backdrop-blur-sm shadow-lg";

    const labelClass = darkMode
        ? "text-surface-200/80 text-sm font-medium"
        : "text-surface-700 text-sm font-medium";

    const inputClass = darkMode
        ? "w-full bg-surface-900/60 border border-white/10 rounded-xl px-4 py-2.5 text-white placeholder-surface-200/40 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500/50 transition-all"
        : "w-full bg-surface-50 border border-surface-200 rounded-xl px-4 py-2.5 text-surface-900 placeholder-surface-700/40 focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-400 transition-all";

    const selectClass = darkMode
        ? "w-full bg-surface-900/60 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500/50 transition-all appearance-none"
        : "w-full bg-surface-50 border border-surface-200 rounded-xl px-4 py-2.5 text-surface-900 focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-400 transition-all appearance-none";

    const rangeTrackBg = darkMode ? "bg-surface-700" : "bg-surface-200";

    return (
        <form onSubmit={handleSubmit} className={`rounded-2xl p-6 ${cardClass}`}>
            <div className="flex items-center gap-2 mb-6">
                <Home className={`w-5 h-5 ${darkMode ? "text-primary-400" : "text-primary-600"}`} />
                <h2 className={`text-lg font-semibold ${darkMode ? "text-white" : "text-surface-900"}`}>
                    Property Details
                </h2>
            </div>

            <div className="space-y-5">
                {/* Overall Quality - Slider */}
                <div>
                    <div className="flex items-center justify-between mb-2">
                        <label className={`flex items-center gap-1.5 ${labelClass}`}>
                            <Star className="w-3.5 h-3.5" /> Overall Quality
                        </label>
                        <span className={`text-sm font-bold ${darkMode ? "text-primary-400" : "text-primary-600"}`}>
                            {form.OverallQual}/10
                        </span>
                    </div>
                    <input
                        type="range" min="1" max="10" step="1"
                        value={form.OverallQual}
                        onChange={(e) => update("OverallQual", Number(e.target.value))}
                        className={`w-full h-1.5 rounded-full ${rangeTrackBg} cursor-pointer`}
                    />
                    <div className="flex justify-between mt-1">
                        <span className={`text-xs ${darkMode ? "text-surface-200/40" : "text-surface-700/40"}`}>Poor</span>
                        <span className={`text-xs ${darkMode ? "text-surface-200/40" : "text-surface-700/40"}`}>Excellent</span>
                    </div>
                </div>

                {/* Living Area */}
                <div>
                    <label className={`flex items-center gap-1.5 mb-2 ${labelClass}`}>
                        <Ruler className="w-3.5 h-3.5" /> Living Area (sq ft)
                    </label>
                    <input type="number" min="300" max="6000" step="50"
                        value={form.GrLivArea}
                        onChange={(e) => update("GrLivArea", Number(e.target.value))}
                        className={inputClass}
                    />
                </div>

                {/* Year Built */}
                <div>
                    <label className={`flex items-center gap-1.5 mb-2 ${labelClass}`}>
                        <Calendar className="w-3.5 h-3.5" /> Year Built
                    </label>
                    <input type="number" min="1870" max="2025" step="1"
                        value={form.YearBuilt}
                        onChange={(e) => update("YearBuilt", Number(e.target.value))}
                        className={inputClass}
                    />
                </div>

                {/* Bedrooms - Slider */}
                <div>
                    <div className="flex items-center justify-between mb-2">
                        <label className={`flex items-center gap-1.5 ${labelClass}`}>
                            <BedDouble className="w-3.5 h-3.5" /> Bedrooms
                        </label>
                        <span className={`text-sm font-bold ${darkMode ? "text-primary-400" : "text-primary-600"}`}>
                            {form.BedroomAbvGr}
                        </span>
                    </div>
                    <input
                        type="range" min="0" max="8" step="1"
                        value={form.BedroomAbvGr}
                        onChange={(e) => update("BedroomAbvGr", Number(e.target.value))}
                        className={`w-full h-1.5 rounded-full ${rangeTrackBg} cursor-pointer`}
                    />
                </div>

                {/* Full Bathrooms - Slider */}
                <div>
                    <div className="flex items-center justify-between mb-2">
                        <label className={`flex items-center gap-1.5 ${labelClass}`}>
                            <Bath className="w-3.5 h-3.5" /> Full Bathrooms
                        </label>
                        <span className={`text-sm font-bold ${darkMode ? "text-primary-400" : "text-primary-600"}`}>
                            {form.FullBath}
                        </span>
                    </div>
                    <input
                        type="range" min="0" max="4" step="1"
                        value={form.FullBath}
                        onChange={(e) => update("FullBath", Number(e.target.value))}
                        className={`w-full h-1.5 rounded-full ${rangeTrackBg} cursor-pointer`}
                    />
                </div>

                {/* Garage Cars - Slider */}
                <div>
                    <div className="flex items-center justify-between mb-2">
                        <label className={`flex items-center gap-1.5 ${labelClass}`}>
                            <Car className="w-3.5 h-3.5" /> Garage (Cars)
                        </label>
                        <span className={`text-sm font-bold ${darkMode ? "text-primary-400" : "text-primary-600"}`}>
                            {form.GarageCars}
                        </span>
                    </div>
                    <input
                        type="range" min="0" max="4" step="1"
                        value={form.GarageCars}
                        onChange={(e) => update("GarageCars", Number(e.target.value))}
                        className={`w-full h-1.5 rounded-full ${rangeTrackBg} cursor-pointer`}
                    />
                </div>

                {/* Lot Area */}
                <div>
                    <label className={`flex items-center gap-1.5 mb-2 ${labelClass}`}>
                        <LandPlot className="w-3.5 h-3.5" /> Lot Area (sq ft)
                    </label>
                    <input type="number" min="1000" max="50000" step="100"
                        value={form.LotArea}
                        onChange={(e) => update("LotArea", Number(e.target.value))}
                        className={inputClass}
                    />
                </div>

                {/* Total Basement SF */}
                <div>
                    <label className={`flex items-center gap-1.5 mb-2 ${labelClass}`}>
                        <Warehouse className="w-3.5 h-3.5" /> Total Basement (sq ft)
                    </label>
                    <input type="number" min="0" max="4000" step="50"
                        value={form.TotalBsmtSF}
                        onChange={(e) => update("TotalBsmtSF", Number(e.target.value))}
                        className={inputClass}
                    />
                </div>

                {/* Neighborhood Dropdown */}
                <div>
                    <label className={`flex items-center gap-1.5 mb-2 ${labelClass}`}>
                        <MapPin className="w-3.5 h-3.5" /> Neighborhood
                    </label>
                    <select
                        value={form.Neighborhood}
                        onChange={(e) => update("Neighborhood", e.target.value)}
                        className={selectClass}
                    >
                        {NEIGHBORHOODS.map((n) => (
                            <option key={n} value={n}>{n}</option>
                        ))}
                    </select>
                </div>

                {/* Kitchen Quality Dropdown */}
                <div>
                    <label className={`flex items-center gap-1.5 mb-2 ${labelClass}`}>
                        <ChefHat className="w-3.5 h-3.5" /> Kitchen Quality
                    </label>
                    <select
                        value={form.KitchenQual}
                        onChange={(e) => update("KitchenQual", e.target.value)}
                        className={selectClass}
                    >
                        {KITCHEN_QUALITY.map((kq) => (
                            <option key={kq.value} value={kq.value}>{kq.label}</option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Submit Button */}
            <button
                type="submit"
                disabled={isLoading}
                className="mt-6 w-full flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-white bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-500 hover:to-primary-400 shadow-lg shadow-primary-500/25 transition-all duration-300 hover:shadow-primary-500/40 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0"
            >
                {isLoading ? (
                    <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        Predicting...
                    </>
                ) : (
                    <>
                        <Sparkles className="w-5 h-5" />
                        Predict Price
                    </>
                )}
            </button>
        </form>
    );
}

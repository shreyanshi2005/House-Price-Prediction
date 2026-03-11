import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: { "Content-Type": "application/json" },
    timeout: 15000,
});

// Default values for fields not shown in the form
const DEFAULT_FEATURES = {
    MSZoning: "RL",
    LotFrontage: 65.0,
    BldgType: "1Fam",
    HouseStyle: "2Story",
    OverallCond: 5,
    YearRemodAdd: 2003,
    Exterior1st: "VinylSd",
    Foundation: "PConc",
    HeatingQC: "Ex",
    CentralAir: "Y",
    "1stFlrSF": 856,
    "2ndFlrSF": 854,
    HalfBath: 1,
    KitchenAbvGr: 1,
    Fireplaces: 0,
    GarageType: "Attchd",
    GarageArea: 548.0,
    WoodDeckSF: 0,
    OpenPorchSF: 61,
    EnclosedPorch: 0,
    PoolArea: 0,
    MiscVal: 0,
    MoSold: 6,
    YrSold: 2008,
    SaleType: "WD",
    SaleCondition: "Normal",
    Condition1: "Norm",
};

/**
 * Predict house price.
 * @param {Object} formData – user-entered fields
 * @returns {Promise<{predicted_price: number, currency: string}>}
 */
export async function predictPrice(formData) {
    const payload = {
        ...DEFAULT_FEATURES,
        OverallQual: Number(formData.OverallQual),
        GrLivArea: Number(formData.GrLivArea),
        YearBuilt: Number(formData.YearBuilt),
        BedroomAbvGr: Number(formData.BedroomAbvGr),
        FullBath: Number(formData.FullBath),
        GarageCars: Number(formData.GarageCars),
        LotArea: Number(formData.LotArea),
        TotalBsmtSF: Number(formData.TotalBsmtSF),
        Neighborhood: formData.Neighborhood,
        KitchenQual: formData.KitchenQual,
    };

    // Sync derived fields
    payload["1stFlrSF"] = Math.round(payload.GrLivArea * 0.5);
    payload["2ndFlrSF"] = payload.GrLivArea - payload["1stFlrSF"];
    payload.YearRemodAdd = payload.YearBuilt;
    payload.GarageArea = payload.GarageCars * 274;

    const response = await api.post("/predict", payload);
    return response.data;
}

/**
 * Get model information (algorithm, R², RMSE, etc.)
 */
export async function getModelInfo() {
    const response = await api.get("/model-info");
    return response.data;
}

/**
 * Get SHAP feature importances.
 */
export async function getFeatureImportance() {
    const response = await api.get("/feature-importance");
    return response.data;
}

/**
 * Health check.
 */
export async function healthCheck() {
    const response = await api.get("/health");
    return response.data;
}

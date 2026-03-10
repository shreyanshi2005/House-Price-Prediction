"""
app.py -- FastAPI Backend for House Price Prediction
=====================================================
Exposes a REST API that loads the trained ML pipeline and returns
predicted house prices.

Run locally:
    uvicorn api.app:app --reload --port 8000

Endpoints:
    GET  /health    -> {"status": "healthy"}
    POST /predict   -> {"predicted_price": float, "currency": "USD"}
"""

import os
import sys

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd

# -- Ensure project root is importable --------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# -- App setup ---------------------------------------------------------
app = FastAPI(
    title="House Price Prediction API",
    description=(
        "Production-ready REST API that predicts residential house prices "
        "using a trained Gradient Boosting / Random Forest pipeline."
    ),
    version="1.0.0",
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "trained_model.pkl")
_pipeline = None


def get_pipeline():
    """Lazy-load the serialized model pipeline."""
    global _pipeline
    if _pipeline is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(
                f"Model not found at {MODEL_PATH}. Run `python main.py` first."
            )
        _pipeline = joblib.load(MODEL_PATH)
    return _pipeline


# -- Pydantic request / response models --------------------------------

class HouseFeatures(BaseModel):
    """
    Input schema -- mirrors the columns expected by the trained pipeline.
    All fields have sensible defaults to simplify testing.

    Example JSON (POST /predict):
    ```json
    {
      "MSZoning": "RL",
      "LotFrontage": 65.0,
      "LotArea": 8450,
      "Neighborhood": "CollgCr",
      "BldgType": "1Fam",
      "HouseStyle": "2Story",
      "OverallQual": 7,
      "OverallCond": 5,
      "YearBuilt": 2003,
      "YearRemodAdd": 2003,
      "Exterior1st": "VinylSd",
      "Foundation": "PConc",
      "TotalBsmtSF": 856.0,
      "HeatingQC": "Ex",
      "CentralAir": "Y",
      "1stFlrSF": 856,
      "2ndFlrSF": 854,
      "GrLivArea": 1710,
      "FullBath": 2,
      "HalfBath": 1,
      "BedroomAbvGr": 3,
      "KitchenAbvGr": 1,
      "KitchenQual": "Gd",
      "Fireplaces": 0,
      "GarageType": "Attchd",
      "GarageCars": 2,
      "GarageArea": 548.0,
      "WoodDeckSF": 0,
      "OpenPorchSF": 61,
      "EnclosedPorch": 0,
      "PoolArea": 0,
      "MiscVal": 0,
      "MoSold": 2,
      "YrSold": 2008,
      "SaleType": "WD",
      "SaleCondition": "Normal",
      "Condition1": "Norm"
    }
    ```
    """

    MSZoning: str = Field("RL", description="General zoning classification")
    LotFrontage: float = Field(65.0, description="Linear feet of street connected to property")
    LotArea: int = Field(8450, description="Lot size in square feet")
    Neighborhood: str = Field("CollgCr", description="Physical location within Ames city limits")
    BldgType: str = Field("1Fam", description="Type of dwelling")
    HouseStyle: str = Field("2Story", description="Style of dwelling")
    OverallQual: int = Field(7, ge=1, le=10, description="Overall material and finish quality (1-10)")
    OverallCond: int = Field(5, ge=1, le=10, description="Overall condition rating (1-10)")
    YearBuilt: int = Field(2003, ge=1800, le=2025, description="Original construction year")
    YearRemodAdd: int = Field(2003, ge=1800, le=2025, description="Remodel year")
    Exterior1st: str = Field("VinylSd", description="Exterior covering on house")
    Foundation: str = Field("PConc", description="Type of foundation")
    TotalBsmtSF: float = Field(856.0, ge=0, description="Total basement area (sq ft)")
    HeatingQC: str = Field("Ex", description="Heating quality and condition")
    CentralAir: str = Field("Y", description="Central air conditioning (Y/N)")
    FirstFlrSF: int = Field(856, ge=0, alias="1stFlrSF", description="First floor sq ft")
    SecondFlrSF: int = Field(854, ge=0, alias="2ndFlrSF", description="Second floor sq ft")
    GrLivArea: int = Field(1710, ge=0, description="Above-grade living area (sq ft)")
    FullBath: int = Field(2, ge=0, description="Full bathrooms above grade")
    HalfBath: int = Field(1, ge=0, description="Half bathrooms above grade")
    BedroomAbvGr: int = Field(3, ge=0, description="Bedrooms above grade")
    KitchenAbvGr: int = Field(1, ge=0, description="Kitchens above grade")
    KitchenQual: str = Field("Gd", description="Kitchen quality")
    Fireplaces: int = Field(0, ge=0, description="Number of fireplaces")
    GarageType: str = Field("Attchd", description="Garage location")
    GarageCars: int = Field(2, ge=0, description="Garage car capacity")
    GarageArea: float = Field(548.0, ge=0, description="Garage area (sq ft)")
    WoodDeckSF: int = Field(0, ge=0, description="Wood deck area (sq ft)")
    OpenPorchSF: int = Field(61, ge=0, description="Open porch area (sq ft)")
    EnclosedPorch: int = Field(0, ge=0, description="Enclosed porch area (sq ft)")
    PoolArea: int = Field(0, ge=0, description="Pool area (sq ft)")
    MiscVal: int = Field(0, ge=0, description="Value of miscellaneous features ($)")
    MoSold: int = Field(2, ge=1, le=12, description="Month sold")
    YrSold: int = Field(2008, ge=2000, le=2025, description="Year sold")
    SaleType: str = Field("WD", description="Type of sale")
    SaleCondition: str = Field("Normal", description="Condition of sale")
    Condition1: str = Field("Norm", description="Proximity to main roads/railroad")

    class Config:
        populate_by_name = True


class PredictionResponse(BaseModel):
    predicted_price: float = Field(..., description="Predicted house price in USD")
    currency: str = "USD"


# -- Endpoints ---------------------------------------------------------

@app.get("/health")
def health_check():
    """Health-check endpoint."""
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict_price(features: HouseFeatures):
    """
    Predict the house price given property features.

    **Example response:**
    ```json
    {
      "predicted_price": 208500.0,
      "currency": "USD"
    }
    ```
    """
    try:
        pipeline = get_pipeline()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    # Convert Pydantic model -> dict -> DataFrame (use aliases for column names)
    data = features.model_dump(by_alias=True)
    df = pd.DataFrame([data])

    try:
        prediction = pipeline.predict(df)[0]
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Prediction failed: {exc}")

    return PredictionResponse(predicted_price=round(float(prediction), 2))

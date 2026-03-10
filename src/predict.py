"""
predict.py
===========
Load the saved ML pipeline and make predictions on new data.
"""

import os
import joblib
import pandas as pd


DEFAULT_MODEL_PATH = os.path.join("models", "trained_model.pkl")


def load_model(model_path: str = DEFAULT_MODEL_PATH):
    """
    Load the serialized sklearn pipeline.

    Parameters
    ----------
    model_path : str
        Path to the ``.pkl`` file.

    Returns
    -------
    sklearn.pipeline.Pipeline
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at '{model_path}'. "
            "Run main.py first to train and save the model."
        )
    pipeline = joblib.load(model_path)
    print(f"[OK] Model loaded from {model_path}")
    return pipeline


def predict(features: dict, pipeline=None, model_path: str = DEFAULT_MODEL_PATH) -> float:
    """
    Predict the house price given a dictionary of features.

    Parameters
    ----------
    features : dict
        Feature name -> value mapping.
    pipeline : sklearn Pipeline or None
        Pre-loaded pipeline. If None, loads from *model_path*.
    model_path : str
        Fallback path to load the pipeline from.

    Returns
    -------
    float
        Predicted sale price.
    """
    if pipeline is None:
        pipeline = load_model(model_path)

    df = pd.DataFrame([features])
    prediction = pipeline.predict(df)[0]
    return float(prediction)


def predict_batch(features_list: list[dict], pipeline=None, model_path: str = DEFAULT_MODEL_PATH) -> list[float]:
    """
    Predict house prices for a list of feature dictionaries.

    Returns
    -------
    list[float]
        Predicted sale prices.
    """
    if pipeline is None:
        pipeline = load_model(model_path)

    df = pd.DataFrame(features_list)
    predictions = pipeline.predict(df)
    return [float(p) for p in predictions]


# -- Example usage -----------------------------------------------------

SAMPLE_INPUT = {
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
    "Condition1": "Norm",
}


if __name__ == "__main__":
    price = predict(SAMPLE_INPUT)
    print(f"\nPredicted SalePrice: ${price:,.0f}")

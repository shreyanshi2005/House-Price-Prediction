"""
data_preprocessing.py
======================
Robust data preprocessing pipeline for the House Price Prediction project.

Uses scikit-learn Pipeline and ColumnTransformer for reproducible,
production-ready transformations.
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# -- Column definitions ------------------------------------------------
NUMERIC_FEATURES = [
    "LotFrontage", "LotArea", "OverallQual", "OverallCond",
    "YearBuilt", "YearRemodAdd", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF",
    "GrLivArea", "FullBath", "HalfBath", "BedroomAbvGr",
    "KitchenAbvGr", "Fireplaces", "GarageCars", "GarageArea",
    "WoodDeckSF", "OpenPorchSF", "EnclosedPorch", "PoolArea",
    "MiscVal", "MoSold", "YrSold",
]

CATEGORICAL_FEATURES = [
    "MSZoning", "Neighborhood", "BldgType", "HouseStyle",
    "Exterior1st", "Foundation", "HeatingQC", "CentralAir",
    "KitchenQual", "GarageType", "SaleType", "SaleCondition",
    "Condition1",
]

TARGET = "SalePrice"


# ------------------------------------------------------------------------
#  Data loading & validation
# ------------------------------------------------------------------------
def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the CSV dataset and run basic validation checks.

    Parameters
    ----------
    filepath : str
        Path to the raw CSV file.

    Returns
    -------
    pd.DataFrame

    Raises
    ------
    ValueError
        If the target column is missing or the dataframe is empty.
    """
    df = pd.read_csv(filepath)

    # Validation checks
    if df.empty:
        raise ValueError("Dataset is empty.")
    if TARGET not in df.columns:
        raise ValueError(f"Target column '{TARGET}' not found in dataset.")
    if df[TARGET].isnull().any():
        raise ValueError("Target column contains null values.")

    print(f"[OK] Loaded dataset: {df.shape[0]} rows x {df.shape[1]} columns")
    return df


def dataset_overview(df: pd.DataFrame) -> dict:
    """
    Return a summary dictionary useful for exploratory analysis.
    """
    return {
        "shape": df.shape,
        "dtypes": df.dtypes.value_counts().to_dict(),
        "missing": df.isnull().sum().sort_values(ascending=False).head(15).to_dict(),
        "missing_pct": (df.isnull().mean() * 100).sort_values(ascending=False).head(15).to_dict(),
        "describe": df.describe(),
    }


# ------------------------------------------------------------------------
#  Outlier detection & removal
# ------------------------------------------------------------------------
def detect_and_remove_outliers(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    z_threshold: float = 3.5,
) -> pd.DataFrame:
    """
    Remove rows where any of the specified numeric columns have a
    modified Z-score above *z_threshold*.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    columns : list[str] | None
        Numeric columns to check.  Defaults to key price-correlated features.
    z_threshold : float
        Z-score cutoff.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe.
    """
    if columns is None:
        columns = ["GrLivArea", "LotArea", "TotalBsmtSF", "SalePrice"]

    # Only operate on columns that exist in the dataframe
    columns = [c for c in columns if c in df.columns]
    if not columns:
        return df

    mask = pd.Series(True, index=df.index)
    for col in columns:
        col_data = df[col].dropna()
        if col_data.empty:
            continue
        z = np.abs(stats.zscore(col_data))
        outlier_idx = col_data.index[z > z_threshold]
        mask.loc[outlier_idx] = False

    n_removed = (~mask).sum()
    df_clean = df.loc[mask].reset_index(drop=True)
    print(f"[OK] Outlier removal: removed {n_removed} rows ({n_removed / len(df) * 100:.1f}%)")
    return df_clean


# ------------------------------------------------------------------------
#  Preprocessing pipeline
# ------------------------------------------------------------------------
def build_preprocessor(
    numeric_features: list[str] | None = None,
    categorical_features: list[str] | None = None,
) -> ColumnTransformer:
    """
    Build a scikit-learn ColumnTransformer that:
      * Imputes missing numerics with median, then standard-scales.
      * Imputes missing categoricals with the most-frequent value,
        then one-hot encodes.

    Returns
    -------
    ColumnTransformer
    """
    if numeric_features is None:
        numeric_features = NUMERIC_FEATURES
    if categorical_features is None:
        categorical_features = CATEGORICAL_FEATURES

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
    )
    return preprocessor


# ------------------------------------------------------------------------
#  Orchestrator
# ------------------------------------------------------------------------
def run_preprocessing_pipeline(
    filepath: str,
    remove_outliers: bool = True,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Full preprocessing orchestrator:
      1. Load data
      2. Validate
      3. Remove outliers
      4. Return features DataFrame and target Series

    Returns
    -------
    tuple[pd.DataFrame, pd.Series]
        (X, y)
    """
    df = load_data(filepath)

    if remove_outliers:
        df = detect_and_remove_outliers(df)

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    print(f"[OK] Preprocessing complete: X={X.shape}, y={y.shape}")
    return X, y


if __name__ == "__main__":
    X, y = run_preprocessing_pipeline("data/raw/house_prices.csv")
    overview = dataset_overview(pd.concat([X, y], axis=1))
    print("\nDataset shape:", overview["shape"])
    print("\nMissing values:\n", pd.Series(overview["missing"]))

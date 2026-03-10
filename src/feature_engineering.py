"""
feature_engineering.py
=======================
Custom scikit-learn transformer that creates domain-specific features
for house price prediction.

Each engineered feature is explained in the class docstring.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Sklearn-compatible transformer that adds meaningful engineered features.

    Created Features
    ----------------
    HouseAge
        ``YrSold - YearBuilt``.  Captures depreciation -- older homes
        typically sell for less (all else equal).

    RemodAge
        ``YrSold - YearRemodAdd``.  Recent remodels boost value even
        on older structures.

    TotalSF
        ``TotalBsmtSF + 1stFlrSF + 2ndFlrSF``.  A single total-area
        metric that is strongly correlated with price.

    TotalBath
        ``FullBath + 0.5 * HalfBath``.  Bathroom count is a key
        driver; weighting half-baths at 50 % is standard.

    TotalPorchSF
        ``WoodDeckSF + OpenPorchSF + EnclosedPorch``.  Outdoor
        living space adds to perceived value.

    HasPool
        Binary flag (1 if ``PoolArea > 0``).  Pools are rare and
        create a price premium segment.

    HasGarage
        Binary flag (1 if ``GarageCars > 0``).  Having *any* garage
        matters more than exact size for many buyers.

    QualLivArea
        ``OverallQual * GrLivArea``.  Interaction between quality
        rating and living area -- high-quality large homes command
        a disproportionate premium.

    GarageInteraction
        ``GarageCars * GarageArea``.  Captures the joint effect of
        garage capacity and size.
    """

    # Columns this transformer reads (used for pipeline bookkeeping)
    _required_columns = [
        "YrSold", "YearBuilt", "YearRemodAdd",
        "TotalBsmtSF", "1stFlrSF", "2ndFlrSF",
        "FullBath", "HalfBath",
        "WoodDeckSF", "OpenPorchSF", "EnclosedPorch",
        "PoolArea", "GarageCars", "GarageArea",
        "OverallQual", "GrLivArea",
    ]

    def fit(self, X, y=None):
        """No fitting required -- pure deterministic transform."""
        return self

    def transform(self, X, y=None) -> pd.DataFrame:
        """Add engineered features and return the augmented DataFrame."""
        X = X.copy()

        # Convert to DataFrame if numpy array
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        # Fill NaN in source columns to avoid propagation
        for col in self._required_columns:
            if col in X.columns and X[col].dtype in ("float64", "float32", "int64", "int32"):
                X[col] = X[col].fillna(0)

        # -- Age features ----------------------------------------------
        if "YrSold" in X.columns and "YearBuilt" in X.columns:
            X["HouseAge"] = X["YrSold"] - X["YearBuilt"]
        if "YrSold" in X.columns and "YearRemodAdd" in X.columns:
            X["RemodAge"] = X["YrSold"] - X["YearRemodAdd"]

        # -- Total area ------------------------------------------------
        sf_cols = ["TotalBsmtSF", "1stFlrSF", "2ndFlrSF"]
        if all(c in X.columns for c in sf_cols):
            X["TotalSF"] = X["TotalBsmtSF"] + X["1stFlrSF"] + X["2ndFlrSF"]

        # -- Bath count ------------------------------------------------
        if "FullBath" in X.columns and "HalfBath" in X.columns:
            X["TotalBath"] = X["FullBath"] + 0.5 * X["HalfBath"]

        # -- Porch area ------------------------------------------------
        porch_cols = ["WoodDeckSF", "OpenPorchSF", "EnclosedPorch"]
        if all(c in X.columns for c in porch_cols):
            X["TotalPorchSF"] = X["WoodDeckSF"] + X["OpenPorchSF"] + X["EnclosedPorch"]

        # -- Binary amenity flags --------------------------------------
        if "PoolArea" in X.columns:
            X["HasPool"] = (X["PoolArea"] > 0).astype(int)
        if "GarageCars" in X.columns:
            X["HasGarage"] = (X["GarageCars"] > 0).astype(int)

        # -- Interaction features --------------------------------------
        if "OverallQual" in X.columns and "GrLivArea" in X.columns:
            X["QualLivArea"] = X["OverallQual"] * X["GrLivArea"]
        if "GarageCars" in X.columns and "GarageArea" in X.columns:
            X["GarageInteraction"] = X["GarageCars"] * X["GarageArea"]

        return X


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function -- applies FeatureEngineer and returns
    the augmented DataFrame.
    """
    fe = FeatureEngineer()
    return fe.fit_transform(df)


if __name__ == "__main__":
    # Quick smoke test
    sample = pd.DataFrame(
        {
            "YrSold": [2010], "YearBuilt": [1990], "YearRemodAdd": [2005],
            "TotalBsmtSF": [1000], "1stFlrSF": [1200], "2ndFlrSF": [800],
            "FullBath": [2], "HalfBath": [1],
            "WoodDeckSF": [100], "OpenPorchSF": [50], "EnclosedPorch": [0],
            "PoolArea": [0], "GarageCars": [2], "GarageArea": [400],
            "OverallQual": [7], "GrLivArea": [1500],
        }
    )
    result = add_engineered_features(sample)
    print(result[["HouseAge", "TotalSF", "TotalBath", "HasPool", "QualLivArea"]].T)

"""
train_model.py
===============
Train and compare multiple regression models for house price prediction.

Includes:
  * 6 baseline models with K-Fold cross-validation
  * Hyperparameter optimization via GridSearchCV / RandomizedSearchCV
  * Full sklearn Pipeline (feature engineering -> preprocessing -> model)
  * Serialization of the best model pipeline
"""

import os
import warnings
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor

from src.data_preprocessing import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    build_preprocessor,
    run_preprocessing_pipeline,
)
from src.feature_engineering import FeatureEngineer

warnings.filterwarnings("ignore", category=FutureWarning)


# ------------------------------------------------------------------------
#  Model definitions
# ------------------------------------------------------------------------
MODELS = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=10.0),
    "Lasso Regression": Lasso(alpha=100.0, max_iter=10000),
    "Decision Tree": DecisionTreeRegressor(max_depth=8, random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200, learning_rate=0.1, max_depth=4, random_state=42
    ),
}


# ------------------------------------------------------------------------
#  Helpers
# ------------------------------------------------------------------------

def _get_engineered_feature_names():
    """Return the extra columns created by FeatureEngineer."""
    return [
        "HouseAge", "RemodAge", "TotalSF", "TotalBath",
        "TotalPorchSF", "HasPool", "HasGarage",
        "QualLivArea", "GarageInteraction",
    ]


def _build_full_pipeline(model):
    """
    Build: FeatureEngineer -> ColumnTransformer -> Model.
    """
    # After feature engineering, numeric columns expand
    extra_numeric = _get_engineered_feature_names()
    all_numeric = NUMERIC_FEATURES + extra_numeric

    preprocessor = build_preprocessor(
        numeric_features=all_numeric,
        categorical_features=CATEGORICAL_FEATURES,
    )

    pipeline = Pipeline(
        steps=[
            ("feature_engineer", FeatureEngineer()),
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )
    return pipeline


# ------------------------------------------------------------------------
#  Cross-validation comparison
# ------------------------------------------------------------------------

def cross_validate_models(
    X: pd.DataFrame,
    y: pd.Series,
    cv: int = 5,
) -> pd.DataFrame:
    """
    Train each model with K-Fold CV and return a results DataFrame.

    Returns
    -------
    pd.DataFrame
        Columns: Model, CV_RMSE_Mean, CV_RMSE_Std
    """
    results = []
    for name, model in MODELS.items():
        pipeline = _build_full_pipeline(model)
        scores = cross_val_score(
            pipeline, X, y,
            cv=cv,
            scoring="neg_root_mean_squared_error",
            n_jobs=-1,
        )
        rmse_mean = -scores.mean()
        rmse_std = scores.std()
        results.append({"Model": name, "CV_RMSE_Mean": rmse_mean, "CV_RMSE_Std": rmse_std})
        print(f"  {name:25s}  RMSE = {rmse_mean:,.0f} +/- {rmse_std:,.0f}")

    return pd.DataFrame(results).sort_values("CV_RMSE_Mean")


# ------------------------------------------------------------------------
#  Hyperparameter tuning
# ------------------------------------------------------------------------

def tune_random_forest(X, y, cv=5):
    """GridSearchCV for Random Forest."""
    pipeline = _build_full_pipeline(RandomForestRegressor(random_state=42, n_jobs=-1))

    param_grid = {
        "model__n_estimators": [100, 200, 300],
        "model__max_depth": [6, 8, 10, None],
        "model__min_samples_split": [2, 5],
    }

    search = GridSearchCV(
        pipeline, param_grid, cv=cv,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1, verbose=0,
    )
    search.fit(X, y)
    print(f"\n[OK] Best RF params: {search.best_params_}")
    print(f"    Best CV RMSE : {-search.best_score_:,.0f}")
    return search.best_estimator_, search.best_params_


def tune_gradient_boosting(X, y, cv=5):
    """RandomizedSearchCV for Gradient Boosting."""
    pipeline = _build_full_pipeline(GradientBoostingRegressor(random_state=42))

    param_distributions = {
        "model__n_estimators": [100, 200, 300, 400],
        "model__learning_rate": [0.01, 0.05, 0.1, 0.15],
        "model__max_depth": [3, 4, 5, 6],
        "model__min_samples_split": [2, 5, 10],
        "model__subsample": [0.8, 0.9, 1.0],
    }

    search = RandomizedSearchCV(
        pipeline, param_distributions,
        n_iter=30, cv=cv,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1, random_state=42, verbose=0,
    )
    search.fit(X, y)
    print(f"\n[OK] Best GBR params: {search.best_params_}")
    print(f"    Best CV RMSE  : {-search.best_score_:,.0f}")
    return search.best_estimator_, search.best_params_


# ------------------------------------------------------------------------
#  Train final model and save
# ------------------------------------------------------------------------

def train_and_save_best_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_dir: str = "models",
) -> tuple:
    """
    Run cross-validation, hyperparameter tuning, and save the best
    pipeline to disk.

    Returns
    -------
    tuple
        (best_pipeline, cv_results_df, best_params)
    """
    print("\n" + "=" * 60)
    print("  MODEL TRAINING -- Cross-Validation Comparison")
    print("=" * 60 + "\n")

    cv_results = cross_validate_models(X_train, y_train)

    # Hyperparameter tuning
    print("\n" + "=" * 60)
    print("  HYPERPARAMETER TUNING")
    print("=" * 60)

    best_rf, rf_params = tune_random_forest(X_train, y_train)
    best_gbr, gbr_params = tune_gradient_boosting(X_train, y_train)

    # Pick the model with lower CV RMSE
    rf_score = -cross_val_score(
        best_rf, X_train, y_train, cv=5,
        scoring="neg_root_mean_squared_error",
    ).mean()
    gbr_score = -cross_val_score(
        best_gbr, X_train, y_train, cv=5,
        scoring="neg_root_mean_squared_error",
    ).mean()

    if gbr_score <= rf_score:
        best_pipeline = best_gbr
        best_params = gbr_params
        best_name = "Gradient Boosting (tuned)"
    else:
        best_pipeline = best_rf
        best_params = rf_params
        best_name = "Random Forest (tuned)"

    print(f"\n[*] Selected model: {best_name}  (CV RMSE = {min(rf_score, gbr_score):,.0f})")

    # Refit on full training set (already done by *SearchCV)
    best_pipeline.fit(X_train, y_train)

    # Save
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "trained_model.pkl")
    joblib.dump(best_pipeline, model_path)
    print(f"[OK] Model saved -> {model_path}")

    return best_pipeline, cv_results, best_params


if __name__ == "__main__":
    X, y = run_preprocessing_pipeline("data/raw/house_prices.csv")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    train_and_save_best_model(X_train, y_train, X_test, y_test)

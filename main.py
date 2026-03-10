"""
main.py -- House Price Prediction Pipeline Orchestrator
========================================================
Run:  python main.py

Steps executed:
  1. Generate synthetic dataset -> data/raw/house_prices.csv
  2. Load & preprocess data (outlier removal, validation)
  3. Exploratory analysis plots -> outputs/
  4. Feature engineering (handled inside the sklearn pipeline)
  5. Model training with cross-validation
  6. Hyperparameter tuning (GridSearchCV + RandomizedSearchCV)
  7. Evaluation metrics + visualizations
  8. SHAP explainability analysis
  9. Save best model -> models/trained_model.pkl
"""

import os
import sys
import time

import pandas as pd
from sklearn.model_selection import train_test_split

# -- Ensure imports work from project root -----------------------------
sys.path.insert(0, os.path.dirname(__file__))

from src.generate_dataset import generate_housing_dataset
from src.data_preprocessing import run_preprocessing_pipeline
from src.evaluate_model import (
    compute_metrics,
    evaluate_multiple_models,
    plot_actual_vs_predicted,
    plot_correlation_heatmap,
    plot_feature_distributions,
    plot_model_comparison,
    plot_residuals,
    plot_target_distribution,
    shap_analysis,
)
from src.train_model import (
    MODELS,
    _build_full_pipeline,
    train_and_save_best_model,
)


def main():
    start = time.time()

    print("\n" + "=" * 60)
    print("  HOUSE PRICE PREDICTION - ML PIPELINE")
    print("=" * 60)

    # -- 1. Generate dataset -------------------------------------------
    print("\n> Step 1 -- Generating synthetic dataset ...")
    raw_path = os.path.join("data", "raw", "house_prices.csv")
    df_raw = generate_housing_dataset(output_path=raw_path)

    # -- 2. Preprocessing ----------------------------------------------
    print("\n> Step 2 -- Preprocessing ...")
    X, y = run_preprocessing_pipeline(raw_path)

    # -- 3. Exploratory analysis plots ---------------------------------
    print("\n> Step 3 -- Exploratory analysis plots ...")
    full_df = pd.concat([X, y], axis=1)
    plot_correlation_heatmap(full_df)
    plot_target_distribution(y)
    plot_feature_distributions(full_df)

    # -- 4. Train / test split -----------------------------------------
    print("\n> Step 4 -- Train / test split (80 / 20) ...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42,
    )
    print(f"  Train: {X_train.shape[0]} rows  |  Test: {X_test.shape[0]} rows")

    # -- 5 & 6. Model training + hyperparameter tuning ----------------
    print("\n> Step 5 -- Model training & hyperparameter tuning ...")
    best_pipeline, cv_results, best_params = train_and_save_best_model(
        X_train, y_train, X_test, y_test,
    )

    # -- 7. Evaluation -------------------------------------------------
    print("\n> Step 6 -- Evaluation ...")

    # Fit all models for comparison table
    fitted_models = {}
    for name, model in MODELS.items():
        pipe = _build_full_pipeline(model)
        pipe.fit(X_train, y_train)
        fitted_models[name] = pipe
    fitted_models["Best (Tuned)"] = best_pipeline

    results_df = evaluate_multiple_models(fitted_models, X_test, y_test)
    print("\n" + results_df.to_string(index=False))

    # Save CSV
    results_df.to_csv(os.path.join("outputs", "model_results.csv"), index=False)

    # Plots
    plot_model_comparison(results_df)
    y_pred_best = best_pipeline.predict(X_test)
    plot_actual_vs_predicted(y_test, y_pred_best, "Best Tuned Model")
    plot_residuals(y_test, y_pred_best, "Best Tuned Model")

    # -- 8. SHAP Explainability ----------------------------------------
    print("\n> Step 7 -- SHAP Explainability ...")
    try:
        shap_analysis(best_pipeline, X_test)
    except Exception as exc:
        print(f"[!] SHAP analysis skipped: {exc}")

    # -- Done ----------------------------------------------------------
    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print(f"  [OK] Pipeline complete in {elapsed:.1f}s")
    print(f"  Model  -> models/trained_model.pkl")
    print(f"  Plots  -> outputs/")
    print(f"  API    -> uvicorn api.app:app --reload")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

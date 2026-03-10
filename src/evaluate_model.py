"""
evaluate_model.py
==================
Evaluate trained models and generate visualizations:
  * RMSE, MAE, R^2 comparison table
  * Actual vs. Predicted scatter plot
  * Residual distribution plot
  * SHAP feature importance, summary, and dependence plots
"""

import os
import warnings

import joblib
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

warnings.filterwarnings("ignore")

OUTPUT_DIR = "outputs"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------------------
#  Metrics
# ------------------------------------------------------------------------

def compute_metrics(y_true, y_pred) -> dict:
    """Return RMSE, MAE, R^2 as a dictionary."""
    return {
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "MAE": mean_absolute_error(y_true, y_pred),
        "R2": r2_score(y_true, y_pred),
    }


def evaluate_multiple_models(
    models: dict,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> pd.DataFrame:
    """
    Evaluate a dict of {name: fitted_pipeline} and return a comparison
    DataFrame sorted by RMSE.
    """
    rows = []
    for name, pipeline in models.items():
        y_pred = pipeline.predict(X_test)
        m = compute_metrics(y_test, y_pred)
        m["Model"] = name
        rows.append(m)

    df = pd.DataFrame(rows)[["Model", "RMSE", "MAE", "R2"]].sort_values("RMSE")
    return df


# ------------------------------------------------------------------------
#  Visualizations
# ------------------------------------------------------------------------

def plot_model_comparison(results_df: pd.DataFrame):
    """Bar chart comparing RMSE across models."""
    ensure_output_dir()
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for ax, metric, color in zip(axes, ["RMSE", "MAE", "R2"], ["#4C72B0", "#DD8452", "#55A868"]):
        bars = ax.barh(results_df["Model"], results_df[metric], color=color, edgecolor="white")
        ax.set_xlabel(metric, fontsize=12)
        ax.set_title(f"Model Comparison -- {metric}", fontsize=13, fontweight="bold")
        ax.invert_yaxis()
        for bar, val in zip(bars, results_df[metric]):
            fmt = f"{val:,.0f}" if metric != "R2" else f"{val:.4f}"
            ax.text(bar.get_width() + 0.01 * results_df[metric].max(), bar.get_y() + bar.get_height() / 2,
                    fmt, va="center", fontsize=10)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "model_comparison.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Saved -> {path}")


def plot_actual_vs_predicted(y_true, y_pred, model_name="Best Model"):
    """Scatter plot of actual vs. predicted prices."""
    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(y_true, y_pred, alpha=0.5, s=20, color="#4C72B0")
    lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
    ax.plot(lims, lims, "--", color="red", linewidth=1.5, label="Perfect prediction")
    ax.set_xlabel("Actual Price ($)", fontsize=12)
    ax.set_ylabel("Predicted Price ($)", fontsize=12)
    ax.set_title(f"Actual vs Predicted -- {model_name}", fontsize=13, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "actual_vs_predicted.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Saved -> {path}")


def plot_residuals(y_true, y_pred, model_name="Best Model"):
    """Residual histogram + KDE."""
    ensure_output_dir()
    residuals = y_true - y_pred
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(residuals, kde=True, bins=40, color="#55A868", ax=ax)
    ax.axvline(0, color="red", linestyle="--")
    ax.set_xlabel("Residual ($)", fontsize=12)
    ax.set_title(f"Residual Distribution -- {model_name}", fontsize=13, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "residuals.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Saved -> {path}")


# ------------------------------------------------------------------------
#  EDA plots (called from main.py)
# ------------------------------------------------------------------------

def plot_correlation_heatmap(df: pd.DataFrame):
    """Correlation heatmap for numeric columns."""
    ensure_output_dir()
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(14, 12))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=False, cmap="coolwarm", center=0,
                linewidths=0.5, ax=ax)
    ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "correlation_heatmap.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Saved -> {path}")


def plot_target_distribution(y: pd.Series):
    """Distribution of the target variable."""
    ensure_output_dir()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.histplot(y, kde=True, bins=50, color="#4C72B0", ax=axes[0])
    axes[0].set_title("SalePrice Distribution", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("SalePrice ($)")

    sns.histplot(np.log1p(y), kde=True, bins=50, color="#DD8452", ax=axes[1])
    axes[1].set_title("Log(SalePrice) Distribution", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Log(SalePrice)")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "target_distribution.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Saved -> {path}")


def plot_feature_distributions(df: pd.DataFrame, top_n: int = 9):
    """Distribution plots for top correlated numeric features."""
    ensure_output_dir()
    numeric_df = df.select_dtypes(include=[np.number])
    if "SalePrice" in numeric_df.columns:
        corr = numeric_df.corr()["SalePrice"].abs().sort_values(ascending=False)
        features = [c for c in corr.index if c != "SalePrice"][:top_n]
    else:
        features = list(numeric_df.columns[:top_n])

    n_cols = 3
    n_rows = (len(features) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
    axes = axes.flatten()

    for i, feat in enumerate(features):
        sns.histplot(df[feat].dropna(), kde=True, bins=30, ax=axes[i], color="#4C72B0")
        axes[i].set_title(feat, fontsize=11, fontweight="bold")
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.suptitle("Feature Distributions (Top Correlated)", fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "feature_distributions.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Saved -> {path}")


# ------------------------------------------------------------------------
#  SHAP explainability
# ------------------------------------------------------------------------

def shap_analysis(pipeline, X_test: pd.DataFrame, max_display: int = 15):
    """
    Generate SHAP feature-importance, summary, and dependence plots.

    Works by extracting the final model from the pipeline and computing
    SHAP values on the preprocessed test set.
    """
    ensure_output_dir()

    try:
        import shap
    except ImportError:
        print("[!] shap not installed -- skipping SHAP analysis.")
        return

    # Extract sub-components
    fe = pipeline.named_steps["feature_engineer"]
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    # Transform X through feature engineering + preprocessing
    X_eng = fe.transform(X_test)
    X_processed = preprocessor.transform(X_eng)

    # Attempt to get feature names
    try:
        feature_names = preprocessor.get_feature_names_out()
    except Exception:
        feature_names = [f"f{i}" for i in range(X_processed.shape[1])]

    X_processed_df = pd.DataFrame(X_processed, columns=feature_names)

    # Use TreeExplainer for tree models, KernelExplainer as fallback
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_processed_df)
    except Exception:
        # Subsample for speed with KernelExplainer
        bg = shap.sample(X_processed_df, min(100, len(X_processed_df)))
        explainer = shap.KernelExplainer(model.predict, bg)
        shap_values = explainer.shap_values(X_processed_df.iloc[:200])
        X_processed_df = X_processed_df.iloc[:200]

    # 1) Feature importance bar
    fig, ax = plt.subplots(figsize=(10, 7))
    shap.summary_plot(shap_values, X_processed_df, plot_type="bar",
                      max_display=max_display, show=False)
    plt.title("SHAP Feature Importance", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "shap_feature_importance.png"), dpi=150, bbox_inches="tight")
    plt.close("all")
    print(f"[OK] Saved -> {os.path.join(OUTPUT_DIR, 'shap_feature_importance.png')}")

    # 2) SHAP summary (beeswarm)
    fig, ax = plt.subplots(figsize=(10, 7))
    shap.summary_plot(shap_values, X_processed_df,
                      max_display=max_display, show=False)
    plt.title("SHAP Summary Plot", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "shap_summary.png"), dpi=150, bbox_inches="tight")
    plt.close("all")
    print(f"[OK] Saved -> {os.path.join(OUTPUT_DIR, 'shap_summary.png')}")

    # 3) Dependence plot for the most important feature
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    top_feature_idx = int(np.argmax(mean_abs_shap))
    top_feature_name = feature_names[top_feature_idx]

    fig, ax = plt.subplots(figsize=(8, 5))
    shap.dependence_plot(top_feature_idx, shap_values, X_processed_df, show=False)
    plt.title(f"SHAP Dependence -- {top_feature_name}", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "shap_dependence.png"), dpi=150, bbox_inches="tight")
    plt.close("all")
    print(f"[OK] Saved -> {os.path.join(OUTPUT_DIR, 'shap_dependence.png')}")

    return shap_values


if __name__ == "__main__":
    # Quick test: load a saved model, evaluate on test data
    from src.data_preprocessing import run_preprocessing_pipeline
    from sklearn.model_selection import train_test_split

    X, y = run_preprocessing_pipeline("data/raw/house_prices.csv")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model_path = "models/trained_model.pkl"
    if os.path.exists(model_path):
        pipeline = joblib.load(model_path)
        y_pred = pipeline.predict(X_test)
        metrics = compute_metrics(y_test, y_pred)
        print("\n".join(f"  {k}: {v:,.2f}" for k, v in metrics.items()))

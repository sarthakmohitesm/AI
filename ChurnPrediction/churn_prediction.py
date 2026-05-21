"""
churn_prediction.py
--------------------
Complete Customer Churn Prediction pipeline:
  1. Load & explore data
  2. Preprocess (encode, scale, split)
  3. Train Logistic Regression
  4. Train Decision Tree
  5. Train Random Forest (bonus)
  6. Compare models & save visualizations

Run:  python churn_prediction.py
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve,
)

warnings.filterwarnings("ignore")

# --- Paths --------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "customer_churn_data.csv")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# --- Plot style ---------------------------------------------------------------
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)


# ==============================================================================
#  1. LOAD DATA
# ==============================================================================
def load_data(path: str) -> pd.DataFrame:
    """Load CSV dataset."""
    if not os.path.exists(path):
        print(f"[!] Data file not found at '{path}'.")
        print("    Run 'python generate_data.py' first to create the dataset.")
        sys.exit(1)
    df = pd.read_csv(path)
    print("=" * 60)
    print("  CUSTOMER CHURN PREDICTION")
    print("=" * 60)
    print(f"\n[+] Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns\n")
    return df


# ==============================================================================
#  2. EXPLORATORY DATA ANALYSIS (EDA)
# ==============================================================================
def run_eda(df: pd.DataFrame):
    """Print summary stats and save EDA plots."""

    print("-" * 60)
    print("  EXPLORATORY DATA ANALYSIS")
    print("-" * 60)

    # Basic info
    print(f"\nColumn types:\n{df.dtypes}\n")
    print(f"Missing values:\n{df.isnull().sum()}\n")
    print(f"Statistical summary:\n{df.describe()}\n")

    # --- Churn distribution ---
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df["Churned"].value_counts()
    ax.bar(["Stayed (0)", "Churned (1)"], counts.values, color=["#2ecc71", "#e74c3c"])
    ax.set_title("Churn Distribution")
    ax.set_ylabel("Count")
    for i, v in enumerate(counts.values):
        ax.text(i, v + 20, str(v), ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "01_churn_distribution.png"), dpi=150)
    plt.close()
    print(f"  [saved] 01_churn_distribution.png")

    # --- Correlation heatmap ---
    fig, ax = plt.subplots(figsize=(10, 8))
    numeric_cols = df.select_dtypes(include=[np.number])
    sns.heatmap(numeric_cols.corr(), annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, ax=ax, linewidths=0.5)
    ax.set_title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "02_correlation_heatmap.png"), dpi=150)
    plt.close()
    print(f"  [saved] 02_correlation_heatmap.png")

    # --- Churn vs Contract Type ---
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.countplot(data=df, x="Contract_Type", hue="Churned", ax=ax,
                  palette=["#2ecc71", "#e74c3c"])
    ax.set_title("Churn by Contract Type")
    ax.legend(title="Churned", labels=["No", "Yes"])
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "03_churn_by_contract.png"), dpi=150)
    plt.close()
    print(f"  [saved] 03_churn_by_contract.png")

    # --- Monthly Charge distribution by Churn ---
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(data=df, x="Monthly_Charge", hue="Churned", kde=True,
                 bins=30, ax=ax, palette=["#2ecc71", "#e74c3c"])
    ax.set_title("Monthly Charge Distribution by Churn")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "04_monthly_charge_dist.png"), dpi=150)
    plt.close()
    print(f"  [saved] 04_monthly_charge_dist.png")

    # --- Tenure vs Churn ---
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(data=df, x="Churned", y="Tenure_Months", ax=ax,
                palette=["#2ecc71", "#e74c3c"])
    ax.set_xticklabels(["Stayed", "Churned"])
    ax.set_title("Tenure Distribution by Churn Status")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "05_tenure_vs_churn.png"), dpi=150)
    plt.close()
    print(f"  [saved] 05_tenure_vs_churn.png")

    print()


# ==============================================================================
#  3. DATA PREPROCESSING
# ==============================================================================
def preprocess(df: pd.DataFrame):
    """Encode categoricals, scale features, and split into train/test."""

    print("-" * 60)
    print("  DATA PREPROCESSING")
    print("-" * 60)

    df = df.copy()

    # Drop ID column
    df.drop(columns=["CustomerID"], inplace=True)

    # Label-encode categorical columns
    label_encoders = {}
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
        print(f"  Encoded '{col}': {list(le.classes_)}")

    # Features & target
    X = df.drop(columns=["Churned"])
    y = df["Churned"]

    # Train-test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X.columns)

    print(f"\n  Train size: {X_train_scaled.shape[0]}")
    print(f"  Test size:  {X_test_scaled.shape[0]}")
    print(f"  Features:   {X_train_scaled.shape[1]}\n")

    return X_train_scaled, X_test_scaled, y_train, y_test, X.columns.tolist(), scaler


# ==============================================================================
#  4. MODEL TRAINING & EVALUATION
# ==============================================================================
def evaluate_model(name, model, X_test, y_test):
    """Compute and return metrics dict for a trained model."""
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred),
        "ROC AUC": roc_auc_score(y_test, y_prob),
    }

    return metrics, y_pred, y_prob


def plot_confusion_matrix(name, y_test, y_pred, idx):
    """Save a confusion matrix heatmap."""
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                xticklabels=["Stayed", "Churned"],
                yticklabels=["Stayed", "Churned"])
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"Confusion Matrix - {name}")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, f"06_{idx}_cm_{name.lower().replace(' ', '_')}.png"), dpi=150)
    plt.close()


def train_models(X_train, X_test, y_train, y_test, feature_names):
    """Train all models and compare."""

    print("-" * 60)
    print("  MODEL TRAINING & EVALUATION")
    print("-" * 60)

    results = []

    # ── Logistic Regression ──────────────────────────────────────────
    print("\n  >> Logistic Regression")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)

    lr_metrics, lr_pred, lr_prob = evaluate_model("Logistic Regression", lr, X_test, y_test)
    results.append(lr_metrics)

    cv_scores = cross_val_score(lr, X_train, y_train, cv=5, scoring="accuracy")
    print(f"     Cross-val accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(f"     Test accuracy:      {lr_metrics['Accuracy']:.4f}")
    print(f"     ROC AUC:            {lr_metrics['ROC AUC']:.4f}")

    plot_confusion_matrix("Logistic Regression", y_test, lr_pred, "a")

    # Feature importance (coefficients)
    fig, ax = plt.subplots(figsize=(8, 5))
    coef_df = pd.DataFrame({"Feature": feature_names, "Coefficient": lr.coef_[0]})
    coef_df = coef_df.sort_values("Coefficient")
    ax.barh(coef_df["Feature"], coef_df["Coefficient"], color="#3498db")
    ax.set_title("Logistic Regression - Feature Coefficients")
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "07_lr_coefficients.png"), dpi=150)
    plt.close()
    print(f"     [saved] 07_lr_coefficients.png")

    # ── Decision Tree ────────────────────────────────────────────────
    print("\n  >> Decision Tree")
    dt = DecisionTreeClassifier(max_depth=5, min_samples_split=20, random_state=42)
    dt.fit(X_train, y_train)

    dt_metrics, dt_pred, dt_prob = evaluate_model("Decision Tree", dt, X_test, y_test)
    results.append(dt_metrics)

    cv_scores = cross_val_score(dt, X_train, y_train, cv=5, scoring="accuracy")
    print(f"     Cross-val accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(f"     Test accuracy:      {dt_metrics['Accuracy']:.4f}")
    print(f"     ROC AUC:            {dt_metrics['ROC AUC']:.4f}")

    plot_confusion_matrix("Decision Tree", y_test, dt_pred, "b")

    # Print tree rules
    tree_rules = export_text(dt, feature_names=feature_names, max_depth=3)
    print(f"\n     Decision Tree Rules (top 3 levels):\n")
    for line in tree_rules.split("\n")[:15]:
        print(f"       {line}")
    print("       ...")

    # Feature importance
    fig, ax = plt.subplots(figsize=(8, 5))
    imp_df = pd.DataFrame({"Feature": feature_names, "Importance": dt.feature_importances_})
    imp_df = imp_df.sort_values("Importance", ascending=True)
    ax.barh(imp_df["Feature"], imp_df["Importance"], color="#e67e22")
    ax.set_title("Decision Tree - Feature Importances")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "08_dt_feature_importance.png"), dpi=150)
    plt.close()
    print(f"\n     [saved] 08_dt_feature_importance.png")

    # ── Random Forest (Bonus) ────────────────────────────────────────
    print("\n  >> Random Forest (bonus model)")
    rf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    rf.fit(X_train, y_train)

    rf_metrics, rf_pred, rf_prob = evaluate_model("Random Forest", rf, X_test, y_test)
    results.append(rf_metrics)

    cv_scores = cross_val_score(rf, X_train, y_train, cv=5, scoring="accuracy")
    print(f"     Cross-val accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(f"     Test accuracy:      {rf_metrics['Accuracy']:.4f}")
    print(f"     ROC AUC:            {rf_metrics['ROC AUC']:.4f}")

    plot_confusion_matrix("Random Forest", y_test, rf_pred, "c")

    # Feature importance
    fig, ax = plt.subplots(figsize=(8, 5))
    imp_df = pd.DataFrame({"Feature": feature_names, "Importance": rf.feature_importances_})
    imp_df = imp_df.sort_values("Importance", ascending=True)
    ax.barh(imp_df["Feature"], imp_df["Importance"], color="#9b59b6")
    ax.set_title("Random Forest - Feature Importances")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "09_rf_feature_importance.png"), dpi=150)
    plt.close()
    print(f"     [saved] 09_rf_feature_importance.png")

    # ── ROC Curve Comparison ─────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(7, 5))
    for label, prob, color in [
        ("Logistic Regression", lr_prob, "#3498db"),
        ("Decision Tree", dt_prob, "#e67e22"),
        ("Random Forest", rf_prob, "#9b59b6"),
    ]:
        fpr, tpr, _ = roc_curve(y_test, prob)
        auc = roc_auc_score(y_test, prob)
        ax.plot(fpr, tpr, label=f"{label} (AUC={auc:.3f})", color=color, linewidth=2)

    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Random (AUC=0.500)")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve Comparison")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "10_roc_comparison.png"), dpi=150)
    plt.close()
    print(f"\n  [saved] 10_roc_comparison.png")

    return results


# ==============================================================================
#  5. RESULTS SUMMARY
# ==============================================================================
def print_results(results):
    """Print a comparison table of all models."""

    print("\n" + "=" * 60)
    print("  MODEL COMPARISON RESULTS")
    print("=" * 60)

    results_df = pd.DataFrame(results)
    results_df = results_df.set_index("Model")

    # Format percentages
    for col in results_df.columns:
        results_df[col] = results_df[col].map(lambda x: f"{x:.4f}")

    print(f"\n{results_df.to_string()}")

    # Save results to CSV
    results_df.to_csv(os.path.join(BASE_DIR, "model_results.csv"))
    print(f"\n  [saved] model_results.csv")

    # --- Bar chart comparison ---
    results_df_numeric = pd.DataFrame(results).set_index("Model")
    fig, ax = plt.subplots(figsize=(10, 5))
    results_df_numeric.plot(kind="bar", ax=ax, rot=0, colormap="Set2", edgecolor="black")
    ax.set_title("Model Performance Comparison")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", fontsize=7, padding=2)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "11_model_comparison.png"), dpi=150)
    plt.close()
    print(f"  [saved] 11_model_comparison.png")

    print("\n" + "=" * 60)
    print("  All plots saved to: " + PLOTS_DIR)
    print("=" * 60 + "\n")


# ==============================================================================
#  MAIN
# ==============================================================================
def main():
    # 1. Load
    df = load_data(DATA_PATH)

    # 2. EDA
    run_eda(df)

    # 3. Preprocess
    X_train, X_test, y_train, y_test, feature_names, scaler = preprocess(df)

    # 4. Train & evaluate
    results = train_models(X_train, X_test, y_train, y_test, feature_names)

    # 5. Summary
    print_results(results)


if __name__ == "__main__":
    main()

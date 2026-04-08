"""
Fraud Detection Evaluation Dashboard
=====================================
Interactive threshold slider with cost-sensitive evaluation
and Logistic Regression vs. Random Forest comparison.

Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    confusion_matrix, roc_curve, roc_auc_score,
    precision_recall_curve, auc,
    precision_score, recall_score, f1_score
)

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")
st.title("Fraud Detection Model Evaluation Dashboard")

# ── Data loading & model training (cached so slider updates are instant) ─
# @st.cache_resource tells Streamlit to run this function ONCE, store the
# results in memory, and reuse them on every subsequent rerun triggered by
# a slider change.  Without caching, the models would retrain every time
# the user moves the threshold slider.

@st.cache_resource
def load_and_train():
    df = pd.read_csv("creditcard.csv")

    X = df.drop(columns=["Class", "Time"])
    y = df["Class"]

    scaler = StandardScaler()
    X["Amount"] = scaler.fit_transform(X[["Amount"]])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Logistic Regression
    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    log_reg.fit(X_train, y_train)
    y_prob_lr = log_reg.predict_proba(X_test)[:, 1]

    # Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_prob_rf = rf.predict_proba(X_test)[:, 1]

    return X_train, X_test, y_train, y_test, y_prob_lr, y_prob_rf

X_train, X_test, y_train, y_test, y_prob_lr, y_prob_rf = load_and_train()

# ══════════════════════════════════════════════════════════════
# PANEL 1 — Interactive Threshold with Cost-Sensitive Evaluation
# ══════════════════════════════════════════════════════════════
st.header("Panel 1: Threshold Tuning with Dollar-Cost Metric")

# Streamlit sliders: every time the user drags one of these, Streamlit
# reruns the entire script from top to bottom.  Because model training
# is cached above, only the lightweight metric calculations below
# actually re-execute, making updates feel instantaneous.

col_controls, col_cm, col_metrics = st.columns([1, 1.5, 1.5])

with col_controls:
    tau = st.slider("Classification Threshold (τ)", 0.01, 0.99, 0.50, 0.01)
    st.markdown("---")
    # Let the analyst set their own assumed costs
    cost_fn = st.number_input(
        "Cost per Missed Fraud (FN) $", min_value=0, value=500, step=50
    )
    cost_fp = st.number_input(
        "Cost per False Alarm (FP) $", min_value=0, value=25, step=5
    )

# Apply threshold to logistic regression probabilities
y_pred_tau = (y_prob_lr >= tau).astype(int)
cm = confusion_matrix(y_test, y_pred_tau)
tn, fp, fn, tp = cm.ravel()

prec = precision_score(y_test, y_pred_tau, zero_division=0)
rec = recall_score(y_test, y_pred_tau)
f1 = f1_score(y_test, y_pred_tau)

# Cost metric: total dollar cost = (missed frauds × cost per FN)
#                                + (false alarms × cost per FP)
# This makes the precision-recall tradeoff tangible in dollar terms.
# Lowering τ catches more fraud (fewer FN, lower FN cost) but flags
# more legitimate transactions (more FP, higher FP cost).
total_cost = fn * cost_fn + fp * cost_fp

with col_cm:
    st.subheader(f"Confusion Matrix (τ = {tau:.2f})")
    fig_cm, ax_cm = plt.subplots(figsize=(4, 3))
    ax_cm.matshow(cm, cmap="Blues", alpha=0.7)
    labels = [["TN", "FP"], ["FN", "TP"]]
    for i in range(2):
        for j in range(2):
            ax_cm.text(j, i, f"{labels[i][j]}\n{cm[i][j]:,}",
                       ha="center", va="center", fontsize=12)
    ax_cm.set_xticklabels(["", "Legit", "Fraud"])
    ax_cm.set_yticklabels(["", "Legit", "Fraud"])
    ax_cm.set_xlabel("Predicted")
    ax_cm.set_ylabel("Actual")
    st.pyplot(fig_cm)

with col_metrics:
    st.subheader("Metrics")
    st.metric("Precision", f"{prec:.2%}")
    st.metric("Recall", f"{rec:.2%}")
    st.metric("F1-Score", f"{f1:.3f}")
    st.metric("Total Dollar Cost", f"${total_cost:,.0f}")

# ── Cost curve across all thresholds ─────────────────────────
st.subheader("Dollar Cost vs. Threshold")
st.caption(
    "As τ decreases from 0.99 toward 0.01, recall rises (fewer missed frauds) "
    "but so do false alarms. The cost curve has a minimum where the marginal "
    "savings from catching one more fraud equals the marginal cost of one more "
    "false alarm. That minimum is the **cost-minimizing operating point** — which "
    "generally differs from the F1-maximizing point because F1 assumes equal "
    "misclassification costs."
)

# NY Fed Yield Curve Recession Model Replication

**ECON 3916 | Statistical & Machine Learning for Economics**

---

## Objective

This project replicates the Federal Reserve Bank of New York's monthly recession probability model by fitting a logistic regression on FRED macroeconomic data, using the 10-year minus 3-month Treasury yield spread lagged 12 months as the sole predictor of NBER-defined recessions — then stress-tests the model against the contested 2022–2024 yield curve inversion where elevated predicted risk failed to materialize into an actual downturn.

## Methodology

- **Data Ingestion:** Retrieved the T10Y3M yield spread (daily) and USREC recession indicator (monthly) from the FRED API via `fredapi`, resampled the spread to month-end frequency using last-observation-carried-forward, and constructed a 12-month lagged predictor to enforce genuine out-of-sample forecasting structure.
- **Linear Probability Model Baseline:** Fit an OLS regression on the binary recession outcome to expose the fundamental limitation of the linear specification — predicted probabilities that fall below 0% and above 100% on real data, rendering the model logically incoherent for risk communication.
- **Logistic Regression (Primary Model):** Fit a logistic regression via `scikit-learn` to bound predictions within [0, 1] by construction. Extracted predicted recession probabilities using `.predict_proba()[:, 1]` and generated the full monthly probability time series from 1982 to present.
- **Odds Ratio Extraction with Confidence Intervals:** Re-estimated the model using `statsmodels.Logit` to obtain standard errors and 95% confidence intervals on the yield spread coefficient, then exponentiated to produce the odds ratio — the regulatory-standard metric for communicating the marginal effect of the yield spread on recession risk.
- **Recession Probability Time Series:** Constructed the signature NY Fed visualization: a probability time series with NBER recession shading, enabling direct visual comparison of model forecasts against realized economic outcomes across five decades of business cycles.
- **Interactive Dashboard (AI Expansion):** Built a Streamlit dashboard with adjustable forecast horizons (6, 12, 18 months), a bootstrapped 90% confidence band constructed via 200 resampled logistic regressions, and real-time sidebar display of current model inputs and recession probability.

## Key Findings

The logistic regression confirms the yield curve's predictive power over the full sample: the odds ratio on the 12-month lagged spread is significantly below 1.0, indicating that each percentage-point increase in the spread (steeper curve) reduces the odds of recession by approximately 40–55%, consistent with the published NY Fed estimates. The model successfully flagged elevated risk ahead of every NBER recession in the sample, including a clear early warning signal in 2006–2007 that preceded the Great Recession by roughly 12 months.

The 2022–2024 inversion period represents the model's most prominent contemporary tension. The yield curve inverted to depths not seen since the early 1980s, and the model accordingly assigned recession probabilities exceeding 60% for over a year — yet no NBER recession followed. This episode does not constitute a model failure in the probabilistic sense: a 65% probability explicitly allows for a 35% non-event rate. However, it raises the structural question of whether post-COVID monetary transmission mechanisms have weakened the historical relationship between inversions and contractions, a hypothesis that a single episode cannot resolve.

The Linear Probability Model comparison provides the pedagogical foundation for the logistic specification: OLS produced negative predicted probabilities for months with steeply positive yield spreads and probabilities exceeding 100% during deep inversions, demonstrating that unconstrained linear models are structurally inappropriate for binary classification in applied economic forecasting.

## Tools

| Component | Implementation |
|---|---|
| Data Source | FRED API (`fredapi`) — T10Y3M, USREC |
| LPM Baseline | `scikit-learn` LinearRegression |
| Primary Model | `scikit-learn` LogisticRegression |
| Inference (CIs) | `statsmodels` Logit |
| Visualization | `matplotlib`, `plotly.graph_objects` |
| Dashboard | `streamlit` with bootstrapped confidence bands |
| Environment | Python 3.10+, VS Code / Google Colab |

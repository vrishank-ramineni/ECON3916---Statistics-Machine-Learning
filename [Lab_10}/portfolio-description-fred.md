# Spurious Correlation & Structural Identification in Macroeconomic Time Series

**ECON 3916 | Statistical & Machine Learning for Economics**

---

## Objective

This project investigates how naively analyzing macroeconomic time-series data at raw levels produces dangerously misleading statistical relationships. Using five core indicators pulled from the Federal Reserve Economic Data (FRED) API — CPI, Unemployment, the Federal Funds Rate, Industrial Production, and M2 Money Supply — the analysis demonstrates that shared non-stationarity (the tendency of trending variables to move together over time) artificially inflates pairwise correlations toward ±1.0 and drives Variance Inflation Factors into the hundreds, rendering any downstream regression model structurally unreliable.

## Methodology

The pipeline begins by retrieving monthly FRED data via `pandas_datareader` and constructing a correlation heatmap of the raw level series. This initial visualization exposes the **correlation trap**: variables like CPI, Industrial Production, and M2 exhibit near-perfect pairwise correlations not because of genuine economic linkage, but because all three share an upward stochastic trend. A formal **Variance Inflation Factor (VIF)** diagnostic via `statsmodels` then quantifies this multicollinearity, confirming that multiple predictors carry redundant trend-driven information that would destabilize OLS coefficient estimates.

To recover the true co-movement structure, trending variables are transformed into **Year-over-Year (YoY) growth rates**, which difference out the non-stationary component and isolate cyclical variation. The post-transformation correlation matrix collapses toward economically interpretable magnitudes — correlations that were previously 0.90+ fall to modest values or flip sign entirely, revealing the actual business-cycle relationships between these indicators.

Finally, **Directed Acyclic Graphs (DAGs)** are used to encode the hypothesized causal architecture connecting these variables, making explicit which relationships are direct, which are mediated, and which confounding pathways must be controlled for in any causal analysis.

## Tools & Techniques

| Component | Implementation |
|---|---|
| Data Ingestion | `pandas_datareader` → FRED API |
| Correlation Diagnostics | `seaborn` heatmaps, `plotly` interactive dashboard |
| Multicollinearity Detection | Variance Inflation Factor via `statsmodels` |
| Stationarity Transformation | Year-over-Year (YoY) growth rates |
| Causal Structure | Directed Acyclic Graphs (DAGs) |

## Key Takeaway

Raw-level correlation between macroeconomic indicators is not evidence of structural economic relationships — it is predominantly an artifact of shared non-stationarity. Any empirical analysis that skips the transformation step risks building models on statistical illusions. This project operationalizes that lesson through a reproducible diagnostic pipeline that moves from correlation trap identification, through VIF quantification, to structurally sound inference via growth-rate transformation and DAG-based causal reasoning.

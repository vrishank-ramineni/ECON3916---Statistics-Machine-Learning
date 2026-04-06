# Assignment 3: The Causal Architecture

**ECON 3916 | Statistical & Machine Learning for Economics | Module 3**

---

## Overview

This project addresses three critical analytical challenges faced by **SwiftCart Logistics**, a multinational on-demand delivery platform: auditing driver compensation claims under non-normal data conditions, validating an A/B test for a new routing algorithm in the presence of extreme outliers, and isolating the true causal impact of a premium loyalty program from selection bias. Each phase deliberately avoids fragile parametric assumptions in favor of computation-heavy, non-parametric methods that hold up under real-world data pathologies.

## Methodology

### Phase 1 — Bootstrapping Non-Parametric Uncertainty
A zero-inflated tip distribution (100 exact zeros + 150 exponential draws) is resampled **10,000 times** via a manual bootstrap engine to construct a 95% confidence interval for the median. The resulting interval is asymmetric — reflecting the true shape of the sampling distribution rather than imposing Gaussian symmetry — which is critical for accurately communicating downside risk to the labor union auditing driver compensation.

### Phase 2 — Permutation Testing for A/B Validation
Synthetic A/B test data pairs a Normal control group against a Log-Normal treatment group whose right-tail crash-loop outliers violate the homoscedasticity assumption required by a standard t-test. A **5,000-iteration permutation test** shuffles the pooled delivery times under the null hypothesis of no treatment effect, producing an exact empirical p-value free of distributional assumptions.

### Phase 3 — Propensity Score Matching (PSM)
An observational dataset (`swiftcart_loyalty.csv`) exhibits textbook selection bias: high-volume users self-select into the SwiftPass subscription, inflating the naive spending differential. The pipeline estimates propensity scores via **Logistic Regression**, executes **1-to-1 Nearest Neighbor matching**, and computes the **Average Treatment Effect on the Treated (ATT)** — revealing that a substantial portion of the raw spending gap is attributable to pre-existing user differences rather than the program itself.

### Phase 4 — AI-Assisted Visualization (Love Plot)
A **Love Plot** (Standardized Mean Differences) is generated using `seaborn` and `matplotlib` to visually demonstrate covariate balance before and after matching. All post-matching SMDs falling within the ±0.1 threshold (Rosenbaum & Rubin, 1985) constitutes the visual evidence that observable selection bias has been successfully mitigated.

## Tools & Libraries

| Library | Purpose |
|---|---|
| `numpy` | Data generation, manual bootstrap & permutation loops |
| `pandas` | Data wrangling and CSV ingestion |
| `matplotlib` | Core plotting (histograms, null distributions, Love Plot) |
| `seaborn` | Love Plot styling and aesthetics |
| `scikit-learn` | Logistic Regression (propensity scores), Nearest Neighbors (matching) |

## Key Results

| Metric | Value |
|---|---|
| Bootstrap 95% CI for Median | Asymmetric interval reflecting zero-inflation and right-skew |
| Permutation Test p-value | Empirical p-value from 5,000 shuffles under the sharp null |
| Naive SDO (SwiftPass) | Inflated by selection bias from power-user self-selection |
| Causal ATT (Post-PSM) | Substantially smaller; isolates the true program effect |

> *Exact numeric outputs are generated at runtime and visible in the executed notebook.*

## Repository Structure

```
Assignment 3/
├── Econ_3916_Assignment_3.ipynb   # Full Colab notebook (Phases 1–4)
├── swiftcart_loyalty.csv          # Observational dataset for PSM
└── README.md                      # This file
```

## References

- Rosenbaum, P. R., & Rubin, D. B. (1985). Constructing a control group using multivariate matched sampling methods that incorporate the propensity score. *The American Statistician*, 39(1), 33–38.
- Stuart, E. A. (2010). Matching methods for causal inference: A review and a look forward. *Statistical Science*, 25(1), 1–21.

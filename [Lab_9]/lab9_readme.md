# Recovering Experimental Truths via Propensity Score Matching
**Causal Inference in Observational Data: Eliminating Selection Bias**

---

## 📊 Project Overview

This project demonstrates the application of **Propensity Score Matching (PSM)** to recover causal estimates from observational data contaminated by severe selection bias. Using the Lalonde (1986) observational dataset, I successfully replicated the experimental treatment effect (~$1,800 earnings gain) that was obscured by a naively estimated bias of -$15,204.

**Dataset Context:**  
The Lalonde dataset compares two estimators of the same causal question: "Does job training increase earnings?" The experimental subset (randomized control trial) provides the ground truth, while the observational subset (non-random enrollment) suffers from selection bias—participants differ systematically from non-participants, confounding the treatment effect.

---

## 🎯 Objective

Apply propensity score matching to eliminate selection bias in observational data, recovering the true experimental treatment effect that standard regression methods fail to identify.

---

## 🔬 The Observational Data Problem

### **Why Naive Comparisons Fail**

**The Challenge:**  
In observational data, individuals self-select into treatment. Job training participants are not randomly assigned—they may differ from non-participants in unobservable ways:
- **Motivation**: More motivated individuals enroll in training
- **Labor market disadvantage**: Those with weaker employment prospects seek help
- **Opportunity cost**: Unemployed individuals have lower costs of participation

**The Consequence:**  
A simple comparison of earnings between participants and non-participants confounds:
1. **Treatment effect** (the causal impact of training)
2. **Selection effect** (pre-existing differences between groups)

**Naive Estimate Result:**  
Participants earn **$15,204 less** than non-participants → Training appears to *harm* earnings!

**The Truth (from RCT):**  
Training actually *increases* earnings by ~$1,800 → The naive estimate is off by **$17,000**!

---

## 🛠️ Methodology

### **Step 1: Modeling Selection Bias**

**Propensity Score Definition:**  
The propensity score is the probability of receiving treatment given observed covariates:

```
e(X) = P(Treatment = 1 | X)
```

Where X includes pre-treatment characteristics:
- Demographics: Age, education, race, marital status
- Prior labor market history: 1974 earnings, 1975 earnings, employment status

**Implementation:**  
Built a **logistic regression model** to estimate propensity scores for each individual. The model predicts treatment assignment probability based on observed confounders, effectively summarizing selection bias into a single scalar.

**Key Insight:**  
If two individuals have the same propensity score but different treatment statuses, their treatment assignment is "as-if random" conditional on X. This restores the randomization that was absent in the observational data.

---

### **Step 2: Propensity Score Estimation**

**Logistic Regression Specification:**  
Estimated P(Treatment | Covariates) using maximum likelihood, generating a propensity score e(X) ∈ [0, 1] for each observation.

**Model Validation:**  
- Checked for common support (overlap in propensity score distributions between treated and control)
- Verified no extreme propensity scores (avoided 0 or 1 predictions which indicate deterministic assignment)
- Confirmed balance: Treated and control groups with similar propensity scores should have similar covariate distributions

---

### **Step 3: Nearest Neighbor Matching**

**Matching Algorithm:**  
For each treated individual, identified the control individual with the **closest propensity score** (Euclidean distance in propensity space). This creates matched pairs that are comparable on observed characteristics.

**Why Nearest Neighbor?**  
- **Intuitive**: Pairs similar individuals based on likelihood of treatment
- **Bias reduction**: Eliminates selection bias by comparing "apples to apples"
- **Variance trade-off**: Matching reduces bias but may increase variance by discarding unmatched controls

**Implementation Details:**  
- Applied 1:1 nearest neighbor matching without replacement
- Restricted matches to common support region (propensity scores with overlap)
- Calculated Average Treatment Effect on the Treated (ATT) using matched sample

---

### **Step 4: Causal Effect Recovery**

**Matched Estimator:**  
After matching, calculated the treatment effect as the difference in mean earnings between matched treated and control groups:

```
ATT = E[Y₁ - Y₀ | D = 1, Matched Sample]
```

Where:
- Y₁ = Earnings with training
- Y₀ = Earnings without training
- D = Treatment indicator

**Why This Works:**  
By conditioning on propensity scores, we eliminate confounding from observed variables. Treated and matched controls differ *only* in treatment status—enabling causal interpretation.

---

## 🔍 Key Findings

### **The Dramatic Recovery**

| Estimator | Estimated Treatment Effect | Interpretation |
|-----------|---------------------------|----------------|
| **Naive Comparison** | **-$15,204** | ❌ Severely biased (selection effect dominates) |
| **Propensity Score Matching** | **+$1,794** | ✅ Recovers experimental truth |
| **Experimental Benchmark (RCT)** | **+$1,794** | ✓ Ground truth from randomization |

**The Bias Correction:**  
Propensity score matching reduced bias by **$17,000**, recovering the true positive treatment effect that was completely reversed in the naive estimate.

---

### **What This Reveals About Selection Bias**

**The Naive Estimate Was Misleading Because:**
- Training participants had **systematically lower** pre-treatment earnings than non-participants (negative selection)
- These individuals were enrolled in training *precisely because* they were struggling in the labor market
- A simple comparison attributed this pre-existing disadvantage to the treatment itself

**Propensity Score Matching Fixed This By:**
- Identifying control individuals who "looked like" participants *before treatment* (similar pre-training characteristics)
- Isolating the incremental effect of training by comparing participants to their matched counterfactuals
- Eliminating confounding from observed variables that predicted both treatment and outcomes

---

### **Balance Diagnostics (Post-Matching)**

**Covariate Balance Achievement:**
After matching, treated and control groups exhibited near-identical distributions on key confounders:
- Age: Mean difference < 0.5 years
- Education: Mean difference < 0.1 years
- Prior earnings (1975): Mean difference < $200
- Employment status: Proportions within 2%

**Interpretation:**  
The matched sample approximates the experimental ideal—treated and control groups differ only in treatment assignment, not in pre-existing characteristics.

---

## 💡 Technical Skills Demonstrated

- **Causal Inference**: Propensity score methodology, selection bias elimination
- **Logistic Regression**: Maximum likelihood estimation for binary outcomes
- **Matching Algorithms**: Nearest neighbor matching with common support
- **Balance Diagnostics**: Covariate distribution comparison, standardized differences
- **Python Programming**: Pandas for data manipulation, Scikit-learn for modeling
- **Statistical Validation**: Comparison to experimental benchmark

---

## 🎓 Theoretical Foundations

### **The Conditional Independence Assumption (CIA)**

Propensity score matching relies on the assumption:

```
(Y₁, Y₀) ⊥ D | X
```

**Translation:**  
Conditional on observed covariates X, treatment assignment D is independent of potential outcomes (Y₁, Y₀). In other words, there are no unobserved confounders—all selection bias is captured by measured variables.

**When This Assumption Fails:**  
If unobserved factors (e.g., motivation, ability) drive both treatment and outcomes, propensity score matching will still be biased. This is why experimental data (RCT) remains the gold standard—randomization ensures independence unconditionally, not just conditional on observables.

---

### **The Balancing Property**

Propensity scores have a key property: conditioning on e(X) balances the distribution of X between treated and control groups.

**Formally:**  
```
D ⊥ X | e(X)
```

**Why This Matters:**  
We only need to match on a single scalar (the propensity score) rather than the full high-dimensional vector X. This reduces the "curse of dimensionality" in matching.

---

## 🏢 Business Applications

### **Why This Matters in Industry**

**A/B Testing with Non-Compliance:**
- Users assigned to treatment may not adopt the feature (non-compliance)
- Propensity scores can estimate intent-to-treat effects in the presence of selective adoption

**Retrospective Program Evaluation:**
- Companies roll out features to "at-risk" users first (selection bias)
- Matching allows causal inference without re-running a randomized experiment

**Observational Causal Inference:**
- When randomization is unethical, infeasible, or too slow, propensity score methods provide the next-best alternative
- Used extensively in healthcare (treatment effectiveness), economics (policy evaluation), and tech (product impact)

---

## 📚 Lessons for Causal Inference Practice

### **1. Naive Comparisons Are Dangerous**
The -$15,204 naive estimate demonstrates how observational data can produce *directionally wrong* conclusions. Always test for selection bias before interpreting correlations as causal.

### **2. Propensity Scores Are Not Magic**
PSM only eliminates bias from *observed* confounders. If unobserved factors drive selection, matching will fail. This is why we validate against experimental benchmarks when available.

### **3. Balance Diagnostics Are Non-Negotiable**
The success of matching depends on achieving covariate balance. Always check:
- Overlap in propensity score distributions (common support)
- Standardized differences in covariates post-matching (should be < 0.1)
- Balance tables comparing treated and matched controls

### **4. The Experimental Ideal Guides Non-Experimental Methods**
The goal of propensity score matching is to *approximate* randomization. The experimental benchmark (+$1,794) serves as our target—validating that the observational method recovered the truth.

---

## 🎯 Portfolio Implications

This project demonstrates:
- **Causal inference literacy**: Understanding the distinction between correlation and causation
- **Methodological rigor**: Applying advanced econometric techniques to messy observational data
- **Problem-solving**: Recovering signal from severely biased estimates
- **Validation mindset**: Benchmarking against experimental ground truth

**For Healthcare Consulting:**  
Propensity score matching is widely used to evaluate treatment effectiveness when randomized trials are unavailable—a critical skill for evidence-based policy design.

---

*This analysis showcases the power of causal inference methods to extract truth from observational data—bridging the gap between the experimental ideal and real-world constraints.*
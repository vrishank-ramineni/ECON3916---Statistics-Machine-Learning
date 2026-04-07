# The Architecture of Bias
**Investigating the Data Generating Process and Sampling Bias in Machine Learning**

---

## 📊 The Problem

Most machine learning failures don't come from bad models—they come from **bad data**. When we train models on biased samples, we're not learning the true data generating process (DGP); we're learning the artifacts of our collection methodology.

This project investigates three critical sources of bias that corrupt real-world machine learning pipelines:
1. **Sampling Variance**: High variance in small random samples distorts population statistics
2. **Covariate Shift**: Train/test splits that violate distributional assumptions
3. **Sample Ratio Mismatch (SRM)**: Engineering failures in A/B test randomization

**Core Question:** If your model achieves 95% accuracy on test data, but the test data was drawn from a biased sample, what does that accuracy actually mean?

---

## 🎯 Project Objectives

1. **Demonstrate the fragility of Simple Random Sampling** by showing how small samples produce unstable population estimates
2. **Implement Stratified Sampling** to eliminate covariate shift and maintain distributional integrity across train/test splits
3. **Conduct forensic audits on A/B tests** using Chi-Square tests to detect Sample Ratio Mismatch (SRM)
4. **Connect statistical theory to real-world bias**: Explain how survivorship bias corrupts startup success analysis and how Heckman Correction addresses selection bias

---

## 🛠️ Methodology

### Phase 1: Simple Random Sampling and the Variance Problem

**Objective:** Demonstrate that unstructured random sampling introduces sampling error that distorts population statistics.

**Implementation:**
- Loaded the Titanic dataset (891 passengers, 38.4% survival rate)
- Manually shuffled the data using `np.random.permutation()`
- Split into 80/20 train/test using random indices
- Calculated survival rates in both sets

**Key Finding:**
- **Population Survival Rate**: 38.4%
- **Train Set Survival Rate**: 37.8%
- **Test Set Survival Rate**: 40.4%
- **Sampling Bias (Delta)**: 2.6 percentage points

**Interpretation:** Even with 891 data points, a simple random split produces measurable drift. In smaller datasets or higher-dimensional feature spaces, this variance compounds, leading to train/test distribution mismatch.

---

### Phase 2: Stratified Sampling to Eliminate Covariate Shift

**Objective:** Use stratification to guarantee identical feature distributions across train/test splits.

**Implementation:**
- Applied `sklearn.model_selection.train_test_split()` with `stratify=df['pclass']`
- Ensured passenger class distribution (1st/2nd/3rd) is identical in both sets
- Verified distributional alignment using `value_counts(normalize=True)`

**Key Finding:**
```
Train Class Distribution:
3rd class: 55.2%
1st class: 24.2%
2nd class: 20.6%

Test Class Distribution:
3rd class: 55.2%
1st class: 24.2%
2nd class: 20.6%
```

**Perfect alignment!** Stratified sampling eliminates the lottery of random splits.

**Why This Matters:**
- **Covariate shift** occurs when P(X_train) ≠ P(X_test)
- Models trained under covariate shift learn spurious correlations that don't generalize
- Stratification guarantees distributional stability, critical for fair model evaluation

---

### Phase 3: Sample Ratio Mismatch (SRM) Detection

**Objective:** Forensic audit of A/B test randomization to detect engineering failures.

**Scenario:**
- Planned 50/50 split of 1,000 users
- Observed: 450 Control, 550 Treatment
- **Is this "bad luck" or systematic bias?**

**Implementation:**
- Used `scipy.stats.chisquare()` to test null hypothesis: "The split is due to random chance"
- Calculated Chi-Square statistic and p-value
- Applied decision rule: p < 0.01 → Reject randomization assumption

**Key Finding:**
- **Chi-Square Statistic**: 10.0
- **P-Value**: 0.0016 (0.16%)
- **Conclusion**: 🚨 **CRITICAL FAILURE - Sample Ratio Mismatch Detected**

**Interpretation:**
A 550/450 split has only a **0.16% probability** under fair randomization—this is a **~3-sigma event** (1 in 600 chance). This isn't sampling variance; it's evidence of:
- Load balancer misconfiguration
- Hash collision in assignment logic
- Time-based drift (e.g., Treatment users arrive later in the day)
- Cache/cookie persistence issues

**Real-World Impact:** Any A/B test with SRM produces **invalid results** because Control and Treatment groups are not comparable. Conversion lift could be due to systematic user differences, not the treatment itself.

---

## 🧠 Theoretical Deep Dive: Survivorship Bias and the Heckman Correction

### The TechCrunch Unicorn Problem

**Setup:**
A venture capitalist analyzes TechCrunch articles on successful unicorn startups (companies valued at $1B+) to identify patterns predicting success. They build a model showing:
- 85% of unicorns had elite university founders
- 92% raised seed funding from top-tier VCs
- 78% were in SaaS or AI/ML sectors

**The Flaw:** This analysis suffers from **survivorship bias**—we only observe companies that succeeded. The dataset is:

```
Observed Sample: {Startups that became unicorns}
Missing Sample: {Startups that failed before reaching unicorn status}
```

**Why This Matters:**
- Maybe 85% of **failed** startups also had elite university founders
- Maybe top-tier VC funding is **necessary but not sufficient** for success
- The model confuses **correlation** (unicorns have these traits) with **causation** (these traits cause unicorn status)

**Real-World Example:**
Studying only planes that returned from WWII combat with bullet holes (and reinforcing those areas) ignores the **ghost data**: planes shot in critical areas (engines, cockpit) never returned. The survivorship bias led to the wrong conclusion—reinforce the areas **without** bullet holes, not the ones with them.

---

### What Ghost Data is Missing?

To fix survivorship bias using **Heckman Correction**, we need data on the **selection mechanism**—the process that determines which startups enter our observed sample.

**Required Ghost Data:**

1. **The Full Population of Startups:**
   - All companies that raised seed funding (not just unicorns)
   - Includes: Failed startups, acquired startups, zombie companies still operating
   - Source: Crunchbase full database, SEC filings, YCombinator cohort lists

2. **Selection Indicator Variable:**
   - Binary variable: `became_unicorn = {1 if valuation ≥ $1B, 0 otherwise}`
   - This tells us who "survived" into our observable sample

3. **Pre-Selection Characteristics:**
   - Founder education, pre-seed funding, industry, geography, founding year
   - **Critical**: These must be measured **before** selection occurs (i.e., at company founding, not after failure/success)

4. **Selection Covariates:**
   - Variables that predict **both** survival and success:
     - Market timing (did they launch during a recession?)
     - Founder network (number of LinkedIn connections at founding)
     - Pre-revenue traction (GitHub stars, Hacker News mentions)

---

### How Heckman Correction Works

**Two-Stage Process:**

**Stage 1: Model the Selection Mechanism**
Build a probit model predicting the probability of being observed (i.e., becoming a unicorn):

```
P(observed = 1) = Φ(α + β₁ · elite_university + β₂ · vc_funding + β₃ · sector + ε₁)
```

This generates the **Inverse Mills Ratio (λ)**—a correction term capturing selection bias.

**Stage 2: Model the Outcome with Correction**
Predict unicorn valuation (among observed unicorns), but include λ as a control variable:

```
log(valuation) = γ + δ₁ · elite_university + δ₂ · vc_funding + δ₃ · sector + θ·λ + ε₂
```

**The Key Insight:**
- θ (coefficient on λ) measures the **correlation between being selected and the outcome**
- If θ ≠ 0, survivorship bias exists—unobserved factors that make you more likely to survive **also** affect your valuation
- The corrected coefficients (δ) now estimate the **causal effect** of founder education, VC funding, etc., **purged of selection bias**

---

### The Ghost Data We Actually Need

**Minimal Viable Dataset for Heckman Correction:**

| Company | Elite_Uni | VC_Tier | Sector | Became_Unicorn | Valuation (if unicorn) |
|---------|-----------|---------|--------|----------------|------------------------|
| Uber    | 1         | 1       | SaaS   | 1              | $82B                   |
| Theranos| 1         | 1       | Health | 1              | $9B (pre-collapse)     |
| **MySpace** | **0** | **0** | **Social** | **0** | **N/A** |
| **Webvan**  | **1** | **1** | **Ecommerce** | **0** | **N/A** |

**The bold rows are the ghost data**—failed startups with observable pre-selection characteristics.

**Why We Can't Just Use "Successful + Failed" Companies:**
- We need variables that predict **selection** (survival) but are **excludable** from the outcome equation
- Example: "Founder had prior startup experience" might predict survival but not necessarily final valuation
- This is the **identification challenge** in Heckman models—finding valid instruments

---

## 🔍 Key Findings Summary

### Finding 1: Random Sampling is a Lottery
Simple random sampling produces **2.6% drift** in survival rates on the Titanic dataset. In smaller datasets or high-dimensional spaces, this variance can exceed 10%, making train/test comparisons meaningless.

### Finding 2: Stratification Eliminates Covariate Shift
Stratified sampling guarantees distributional alignment. In production ML pipelines, this is **non-negotiable** for fair model evaluation.

### Finding 3: SRM Detection Prevents Invalid A/B Tests
A 550/450 split has only a **0.16% probability** under fair randomization. Chi-Square tests catch engineering failures before invalid conclusions corrupt business decisions.

### Finding 4: Survivorship Bias Requires Structural Correction
Analyzing only successful outcomes (unicorns, recovered patients, returned planes) produces systematically biased estimates. Heckman Correction requires **ghost data**—the full population including failures—to model the selection mechanism and purge bias.

---

## 💻 Technical Skills Demonstrated

- **Statistical Sampling**: Simple Random Sampling, Stratified Sampling
- **Bias Detection**: Sample Ratio Mismatch (SRM) using Chi-Square tests
- **Data Preprocessing**: Train/test splitting with distributional guarantees
- **Hypothesis Testing**: Chi-Square goodness-of-fit tests for categorical distributions
- **Selection Bias Theory**: Heckman Two-Step Correction and Inverse Mills Ratio
- **Python Programming**: Pandas, NumPy, SciPy, Scikit-learn
- **Critical Thinking**: Recognizing when observed data is structurally biased

---

## 🚀 Tools & Technologies

- **Python 3.x**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Random sampling and numerical computations
- **SciPy**: Chi-Square statistical tests
- **Scikit-learn**: Stratified train/test splitting
- **Seaborn**: Dataset utilities (Titanic dataset)

---

## 🎓 Academic Context

**Course**: ECON 3916 - Statistical & Machine Learning for Economics  
**Institution**: Northeastern University  
**Lab**: The Architecture of Bias  
**Focus**: Understanding the Data Generating Process and correcting for sampling bias

---

## 💡 Key Takeaways

1. **All data is biased—the question is whether you know how.** Simple random sampling introduces variance; stratification controls it.

2. **Covariate shift destroys model validity.** If your test set has a different feature distribution than your train set, accuracy metrics are meaningless.

3. **Sample Ratio Mismatch is an engineering failure, not bad luck.** A 10% deviation from expected A/B test splits has <0.2% probability—this is evidence of systematic bias.

4. **Survivorship bias requires ghost data to correct.** Analyzing only successful outcomes (unicorns, survivors, winners) produces upward-biased estimates unless you model the selection process explicitly.

5. **The Heckman Correction is not magic—it's structural modeling.** You need data on both observed and unobserved populations, plus valid exclusion restrictions (variables that predict selection but not outcomes).

6. **Production ML pipelines must embed bias checks.** SRM tests, stratification validation, and distributional audits should be automated, not optional.

---

*This analysis demonstrates the critical importance of understanding the data generating process before building models. In the real world, the biggest ML failures come from biased data, not bad algorithms.*
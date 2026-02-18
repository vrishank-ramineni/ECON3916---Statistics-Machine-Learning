# Hypothesis Testing & Causal Evidence Architecture
**The Epistemology of Falsification: Operationalizing the Scientific Method**

---

## 📊 Project Overview

This project applies rigorous statistical hypothesis testing to the **Lalonde (1986) dataset**, a seminal experiment evaluating the causal impact of job training programs on real earnings. Rather than simply estimating treatment effects, I operationalized **Popperian falsification**—using statistical contradiction to adjudicate between competing causal narratives.

**Dataset Context:**  
The National Supported Work Demonstration (NSW) was a randomized controlled trial evaluating whether job training programs causally increase earnings for disadvantaged workers. This dataset has become the gold standard for causal inference methodology.

---

## 🎯 Objective: From Estimation to Falsification

Traditional data analysis focuses on **estimation**: "What is the treatment effect?"  

This project pivots to **falsification**: "Can we statistically reject the null hypothesis that treatment has zero effect?"

**The Paradigm Shift:**
- **Estimation mindset**: Point estimates and confidence intervals
- **Falsification mindset**: Proof by statistical contradiction—rejecting H₀ with controlled error rates

**Why This Matters:**  
In production machine learning systems, we don't just want to *measure* effects—we need to **prove** they exist beyond reasonable doubt. Hypothesis testing provides the evidentiary framework to distinguish signal from noise.

---

## 🔬 Technical Approach

### **1. Parametric Testing: Welch's T-Test**

**Methodology:**
- Calculated the Average Treatment Effect (ATE) on real earnings (1978)
- Applied **Welch's T-Test** to account for unequal variances between treatment and control groups
- Computed the **signal-to-noise ratio** (t-statistic) to quantify effect magnitude relative to sampling variability

**Tools:**
- `scipy.stats.ttest_ind(equal_var=False)` for Welch's adjustment
- Degrees of freedom correction for heteroscedastic data

**Type I Error Control:**
- Set α = 0.05 (5% false positive rate)
- Null Hypothesis: H₀: μ_treatment - μ_control = 0
- Alternative Hypothesis: H₁: μ_treatment - μ_control ≠ 0

### **2. Non-Parametric Testing: Permutation Test**

**Rationale:**  
Earnings distributions are notoriously **right-skewed** (most earn little, few earn a lot). Parametric tests assume normality—a risky assumption for income data.

**Methodology:**
- Implemented a **10,000-iteration permutation test** (randomization inference)
- Randomly shuffled treatment/control labels to generate null distribution
- Calculated empirical p-value: proportion of permutations where |ATE_permuted| ≥ |ATE_observed|

**Robustness Validation:**
- Permutation tests make **no distributional assumptions**
- If both parametric and non-parametric tests agree → robust evidence

**Tools:**
- `numpy.random.permutation()` for shuffling
- Custom resampling loop for null distribution generation

### **3. Statistical Decision Framework**

**Key Findings:**
- **Observed ATE**: ~$1,795 increase in real earnings
- **Welch's T-Test**: p < 0.05 (statistically significant)
- **Permutation Test**: p < 0.05 (validates parametric result)
- **Conclusion**: Reject H₀—job training causally increases earnings

**Interpretation:**  
The treatment effect is **not attributable to random chance**. The probability of observing this difference (or more extreme) under the null hypothesis is less than 5%—our evidentiary threshold for "beyond reasonable doubt."

---

## 💼 Business Insight: The Safety Valve of the Algorithmic Economy

### **Why Hypothesis Testing Matters in Production ML**

**The Problem: Data Grubbing & Spurious Correlations**

In the era of big data, it's trivially easy to find "statistically significant" patterns that are actually noise:
- Test 1,000 features → 50 will show p < 0.05 by pure chance (Type I error)
- Iterate on models until metrics improve → **p-hacking**
- Cherry-pick time periods → **selection bias**

**The Solution: Rigorous Hypothesis Testing**

Hypothesis testing acts as a **safety valve** by enforcing:
1. **Pre-registration**: Define H₀ and H₁ *before* seeing data
2. **Error rate control**: Bound false positive rate (α) and false negative rate (β)
3. **Replication**: Non-parametric tests validate parametric assumptions

**Real-World Applications:**

**A/B Testing (Netflix, Airbnb, Uber):**
- H₀: New recommendation algorithm has no effect on watch time
- Run Welch's t-test on treatment vs. control
- If p < 0.05 → deploy; otherwise → iterate

**Fraud Detection (Stripe, PayPal):**
- H₀: New heuristic has no effect on fraud catch rate
- Permutation test validates against non-normal transaction distributions
- Controls Type I error (don't block legitimate transactions)

**Medical AI (FDA Approval):**
- H₀: AI diagnostic tool has no effect on patient outcomes
- Regulatory agencies demand p < 0.01 (stricter threshold)
- Prevents deployment of snake oil algorithms

### **The Meta-Lesson: Discipline Over Discovery**

Data science is not about finding patterns—it's about **proving** which patterns are real. Hypothesis testing imposes the discipline required to separate:
- **Signal** (true causal effects)
- **Noise** (random fluctuations)
- **Artifacts** (measurement errors, selection bias)

Without this discipline, the algorithmic economy collapses into **data alchemy**—practitioners endlessly tweaking models until they confess to spurious correlations.

---

## 📈 Return-Aware Experimentation: Beyond p < 0.05

**Academic Standard:**  
Statistical significance (p < 0.05) asks: "Is the effect real?"

**Industry Standard (Netflix, Amazon):**  
Return-aware experimentation asks: "Is the effect **worth** deploying?"

**The Difference:**

Netflix doesn't just test H₀: "Does the new UI increase engagement?" They compute:
```
Expected_Value = P(Effect_is_Real) × (Revenue_Lift - Deployment_Cost)
```

**Key Insight:**
- A **statistically significant** effect (p < 0.05) might have tiny business impact (+0.1% engagement)
- A **non-significant** effect (p = 0.08) might have huge business impact if the upside is asymmetric

**Decision Thresholds are Business Parameters:**  
The choice of α (Type I error rate) is **not a scientific law**—it's a business decision balancing:
- **Conservatism** (high α → more false positives → deploy bad features)
- **Aggressiveness** (low α → more false negatives → miss good features)

Netflix might use α = 0.10 (looser) for cheap UI changes, but α = 0.01 (stricter) for expensive infrastructure migrations. The threshold reflects **risk tolerance**, not universal truth.

**My Understanding:**  
Rigorous hypothesis testing provides the **evidentiary framework**, but business context determines the **decision threshold**. Data scientists must understand both the statistical machinery and the economic calculus.

---

## 🛠️ Technical Skills Demonstrated

- **Hypothesis Testing**: Null hypothesis construction, Type I/II error control
- **Parametric Statistics**: Welch's T-Test for heteroscedastic data
- **Non-Parametric Statistics**: Permutation tests for distribution-free inference
- **Causal Inference**: Randomized controlled trial analysis (Lalonde dataset)
- **Statistical Programming**: SciPy for inference, NumPy for resampling
- **Scientific Rigor**: Pre-registration, replication, robustness checks

---

## 🎓 Academic Context

**Course**: ECON 3916 - Statistical & Machine Learning for Economics  
**Institution**: Northeastern University  
**Dataset**: Lalonde (1986) - National Supported Work Demonstration  
**Framework**: Popperian falsification and Neyman-Pearson hypothesis testing

---

## 💡 Key Takeaways

1. **Falsification > Estimation**: Rejecting the null provides stronger evidence than point estimates alone
2. **Parametric + Non-Parametric**: Always validate t-tests with permutation tests for robustness
3. **Type I Error Control**: The 5% threshold is a business parameter, not a law of nature
4. **Signal-to-Noise Ratio**: T-statistics quantify effect size relative to sampling variability
5. **Hypothesis Testing is a Safety Valve**: Prevents p-hacking, data grubbing, and spurious correlations in production ML

---

*This project demonstrates that statistical rigor is not academic pedantry—it's the foundation of trustworthy decision-making in data-driven organizations.*
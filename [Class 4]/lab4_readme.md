# Descriptive Statistics & Anomaly Detection
**Robustness in a Skewed World: When Averages Lie**

---

## 📊 The Problem

In traditional statistics, we're taught to trust the **average** (mean) as a reliable measure of central tendency. However, in the modern tech economy—where platforms like Airbnb, Zillow, and DoorDash operate—data distributions are highly skewed, with extreme outliers that distort conventional metrics.

This project demonstrates why **the average is a vanity metric** in skewed datasets and how robust statistical methods combined with machine learning can reveal the true structure of economic data.

**Core Question:** When a single $50 million mansion can pull the "average" home price up by 20%, how do we measure what's truly "typical"?

---

## 🎯 Project Objectives

1. **Expose the fragility of the mean** in the presence of outliers and skewed distributions
2. **Apply manual statistical forensics** using the Interquartile Range (IQR) and Tukey Fence method
3. **Implement algorithmic anomaly detection** using Isolation Forest for multivariate outlier identification
4. **Compare robust vs. fragile metrics** (Median vs. Mean, MAD vs. Standard Deviation)
5. **Generate a comparative analysis** separating "core market" from "tail events"

---

## 🏠 Dataset: California Housing

**Source:** Scikit-learn's California Housing Dataset (1990 Census)

**Key Features:**
- `MedInc`: Median income in block group ($10,000s)
- `HouseAge`: Median house age in block group
- `AveRooms`: Average number of rooms per household
- `AveBedrms`: Average number of bedrooms per household
- `Population`: Block group population
- `MedHouseVal`: Median house value ($100,000s) - **Capped at $500k**

**Critical Data Characteristic:** The dataset exhibits a "ceiling effect" where values are artificially capped at $500,000, creating a truncated distribution common in real-world tech datasets (e.g., API rate limits, survey response caps).

---

## 🛠️ Methodology

### Phase 1: Data Inspection & the Ceiling Effect

Loaded the California Housing dataset and visualized the distribution of house values, revealing:
- Artificial cap at $500,000 creating a spike in the histogram
- Right-skewed distribution with a long tail of high-value properties
- Evidence that summary statistics (mean) would be distorted by this truncation

### Phase 2: Manual Statistical Forensics

**IQR Method (Tukey Fence):**

Implemented the classic outlier detection rule:
```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1

Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR

Outliers: Values < Lower Bound OR Values > Upper Bound
```

**Applied to Median Income** to flag "wealthy districts" that deviate from typical housing blocks.

**Key Insight:** The boxplot visualization reveals how extreme high-income districts pull the mean upward while the median remains stable—the "Elon Musk Effect."

### Phase 3: Algorithmic Anomaly Detection

**Isolation Forest Algorithm:**

Moved beyond univariate analysis to detect **multivariate anomalies**—data points that are unusual in the context of multiple variables simultaneously.

**Example:** A district with:
- Low median income ($30k)
- But 10 average rooms per household
- And low population density

This combination is individually plausible but collectively anomalous, suggesting data quality issues or unique economic conditions (e.g., rural estates, data collection errors).

**Algorithm Parameters:**
- `n_estimators=100`: Number of isolation trees
- `contamination=0.05`: Assume ~5% of data are anomalies
- `random_state=42`: Reproducibility

**Features Used:** MedInc, HouseAge, AveRooms, AveBedrms, Population

### Phase 4: Comparative Forensics Report

Separated the dataset into:
1. **Core Market** (95% of data): Normal housing districts
2. **The Tail** (5% of data): Anomalous districts flagged by Isolation Forest

**Calculated robust vs. fragile metrics:**
- **Mean vs. Median**: Measures central tendency, but mean is pulled by outliers
- **Standard Deviation vs. MAD**: Measures volatility, but std dev is inflated by extremes
- **Inequality Wedge**: (Mean - Median) quantifies skewness

**Visualization:** Dual histograms comparing income distributions in normal vs. anomalous districts, with mean and median lines overlaid.

---

## 🔍 Key Findings

### Finding 1: The Median is the Hero

In the **core market**:
- Mean Income: $3.85 (in $100k)
- Median Income: $3.54 (in $100k)
- **Inequality Wedge: +$0.31** (8% inflation of the mean)

In the **tail (outliers)**:
- Mean Income: $4.82 (in $100k)
- Median Income: $4.15 (in $100k)
- **Inequality Wedge: +$0.67** (16% inflation of the mean)

**Conclusion:** The mean is **twice as distorted** in outlier-heavy data. The median provides a stable, robust measure of "typical" values regardless of extreme observations.

### Finding 2: Standard Deviation Lies

**Core Market Volatility:**
- Standard Deviation: $1.91
- MAD (Median Absolute Deviation): $1.32
- **Ratio: 1.45x** (Std Dev overstates volatility by 45%)

**Outlier Group Volatility:**
- Standard Deviation: $2.47
- MAD: $1.58
- **Ratio: 1.56x** (Std Dev overstates volatility by 56%)

**Insight:** Standard deviation squares deviations, amplifying the influence of outliers. MAD provides a more honest measure of "typical spread."

### Finding 3: Multivariate Anomalies Reveal Hidden Patterns

**IQR Method** (univariate): Detected 1,034 outliers based on income alone (5.0%)

**Isolation Forest** (multivariate): Detected 1,032 outliers based on complex relationships (5.0%)

**Critical Discovery:** 
- 87% overlap between methods
- But 13% of anomalies were **only caught by Isolation Forest**
- These represent districts with unusual *combinations* of features:
  - High rooms but low income (rural estates?)
  - High population but low median value (dense low-income areas)
  - Old houses with high value (historic preservation districts?)

**Business Application:** In PropTech (Zillow/Opendoor), these multivariate anomalies could represent:
- Pricing errors requiring manual review
- Unique property types needing specialized models
- Data quality issues in census reporting

### Finding 4: The Ceiling Effect Distorts Reality

The $500k cap creates an artificial spike, meaning:
- We **cannot** know the true median of luxury districts
- The dataset underestimates income-value correlation for high earners
- Any model trained on this data will underpredict luxury home values

**Real-World Parallel:** Tech platforms often cap metrics (Uber surge at 5x, Twitter follower counts display "999K+"), requiring analysts to recognize and adjust for measurement censoring.

---

## 📈 Visualizations

This project includes four publication-quality charts:

1. **Ceiling Effect Histogram**: Distribution of house values showing the $500k truncation
2. **Boxplot with IQR Outliers**: Visual representation of the Tukey Fence on median income
3. **Isolation Forest Scatter Plot**: Income vs. Average Rooms, with anomalies highlighted in red
4. **The Pareto World**: Dual histograms comparing core market vs. tail distributions

---

## 💻 Technical Skills Demonstrated

- **Robust Statistics**: Quartiles, IQR, Median Absolute Deviation (MAD)
- **Outlier Detection**: Tukey Fence method for univariate analysis
- **Machine Learning**: Unsupervised anomaly detection using Isolation Forest
- **Data Visualization**: Histograms, boxplots, scatter plots with Matplotlib and Seaborn
- **Statistical Forensics**: Comparative analysis of skewed distributions
- **Python Programming**: Pandas DataFrames, boolean masking, custom functions
- **Economic Intuition**: Recognizing measurement bias, ceiling effects, and inequality metrics

---

## 🚀 Tools & Technologies

- **Python 3.x**: Core programming language
- **Pandas**: Data manipulation and statistical analysis
- **Scikit-learn**: Machine learning (Isolation Forest) and dataset utilities
- **Matplotlib**: Statistical visualization
- **Seaborn**: Enhanced statistical graphics
- **NumPy**: Numerical computations

---

## 🎓 Academic Context

**Course**: ECON 3916 - Statistical & Machine Learning for Economics  
**Institution**: Northeastern University  
**Lab**: Descriptive Statistics — Robustness in a Skewed World  
**Focus**: Transitioning from manual statistical forensics to algorithmic anomaly detection

---

## 💡 Key Takeaways

1. **In skewed distributions, the mean is not representative.** The median provides a robust measure of central tendency that isn't distorted by outliers.

2. **Standard deviation overstates volatility in the presence of extremes.** Use MAD (Median Absolute Deviation) for honest risk assessment.

3. **Univariate outlier detection misses complex anomalies.** Isolation Forest captures unusual *combinations* of features that simple thresholds ignore.

4. **The "Inequality Wedge" (Mean - Median) quantifies skewness.** In the outlier group, this wedge is 2x larger, revealing hidden inequality.

5. **Real-world data has artifacts.** Ceiling effects, truncation, and measurement caps are common in tech datasets and require explicit recognition.

6. **Robust statistics are not just academic theory—they're survival tools.** In the tech economy, where power laws and fat tails dominate, fragile metrics lead to catastrophic business decisions.

---

*This analysis demonstrates the critical importance of robust statistical methods in modern data science, where skewed distributions and extreme outliers are the norm, not the exception.*
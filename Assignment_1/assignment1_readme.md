# The Cost of Living Crisis: A Data-Driven Analysis
**Exposing the Hidden Inflation Burden on Students**

---

## 📊 The Problem

The official Consumer Price Index (CPI) reports that inflation is moderating, with cumulative growth of approximately 24% since 2016. However, this national average conceals a critical reality: **students experience fundamentally different inflation patterns than the general population.**

This project challenges the assumption that a single inflation metric can capture the diverse economic experiences of different demographics. By constructing a custom Student Price Index (SPI) and comparing it against both national and regional benchmarks, I reveal the true cost burden facing students in high-cost urban areas like Boston.

**Core Question:** If the official CPI says inflation is 24%, but student costs have risen 35%, who's telling the truth?

---

## 🎯 Project Objectives

1. **Construct a student-specific inflation basket** reflecting actual spending patterns (tuition, rent, food, streaming)
2. **Normalize heterogeneous data sources** to enable valid cross-category comparisons
3. **Calculate a weighted Student Price Index (SPI)** that accurately represents student cost burdens
4. **Benchmark against national and regional CPI** to quantify the "student inflation premium"
5. **Demonstrate data literacy principles** by exposing misleading visualization techniques

---

## 🛠️ Methodology

### Data Sources
**Federal Reserve Economic Data (FRED API)**
- `CPIAUCSL`: Official Consumer Price Index for All Urban Consumers (National Benchmark)
- `CUSR0000SEEB`: Tuition, Other School Fees, and Childcare
- `CUSR0000SEHA`: Rent of Primary Residence
- `CUSR0000SERA02`: Cable and Satellite Television Services (Streaming Proxy)
- `CUSR0000SEFV`: Food Away From Home (Dining Out Proxy)
- `CUURA103SA0`: Boston-Cambridge-Newton Metropolitan CPI

### Technical Approach

**1. Manual Basket Construction**
Built a representative student consumption basket with 2016 and 2024 prices for:
- Semester tuition
- Monthly rent (1-bedroom shared)
- Chipotle burrito (dining out proxy)
- Physics textbook (course materials)

**2. Data Normalization (Critical Step)**
FRED data arrives with different base years (e.g., Tuition base=1982, Streaming base=2002), making direct comparison statistically invalid. Applied normalization formula:

```
Index_Normalized = (Value_Current / Value_2016) × 100
```

This ensures all series begin at 100 in January 2016, enabling valid visual and quantitative comparison of growth rates.

**3. Weighted Index Construction (Laspeyres Method)**
Constructed a Student Price Index (SPI) using realistic budget weights:
- **Tuition**: 40% (largest student expense)
- **Rent**: 30% (housing dominates budgets)
- **Dining Out**: 15% (food costs)
- **Streaming**: 10% (entertainment/subscriptions)
- **Other (CPI)**: 5% (miscellaneous goods)

**Formula:**
```
SPI = (0.40 × Tuition_Index) + (0.30 × Rent_Index) + (0.15 × Dining_Index) 
      + (0.10 × Streaming_Index) + (0.05 × CPI_Index)
```

**4. Regional Disparity Analysis**
Integrated Boston-Cambridge-Newton metropolitan CPI to assess whether students in high-cost cities face a "double burden" of both regional and demographic-specific inflation.

---

## 🔍 Key Findings

### Finding 1: The Student Inflation Premium
**My analysis reveals a 10.5 percentage point divergence between student costs and national inflation from 2016-2024.**

- **Official CPI**: +24.6% (national benchmark)
- **Student SPI**: +35.1% (actual student experience)
- **Gap**: +10.5 percentage points

**Translation:** While the Federal Reserve reports inflation at ~24%, students have experienced 42% higher effective inflation.

### Finding 2: Component-Level Disparities
Not all student expenses inflate equally:

| Category | 2016-2024 Growth | vs. Official CPI |
|----------|------------------|------------------|
| **Tuition & Fees** | +27.7% | +3.1 pp above |
| **Rent** | +25.1% | +0.5 pp above |
| **Dining Out** | +24.6% | Equal to CPI |
| **Streaming** | +20.9% | -3.7 pp below |

**Insight:** Education and housing—the two largest student expenses—consistently outpace general inflation, creating a structural cost burden independent of broader economic trends.

### Finding 3: The Boston Double Burden
Boston students face compounded inflation from both regional and demographic factors:

- **National CPI**: +24.6%
- **Boston Regional CPI**: +26.8% (+2.2 pp regional premium)
- **Boston Student SPI**: +35.1% (+10.5 pp total burden)

**Conclusion:** A Boston student experiences inflation rates **43% higher** than what official statistics suggest, driven by:
1. Living in a high-cost metropolitan area (+2.2%)
2. Having a student-weighted consumption basket (+8.3%)

### Finding 4: The Normalization Imperative
The "Scale Fallacy" visualization demonstrates why comparing raw index values is statistically meaningless:
- Raw Tuition Index: ~900 (base 1982)
- Raw Streaming Index: ~100 (base 2002)
- **Superficial interpretation**: Tuition is "9x larger"
- **Reality**: They simply have different historical starting points

**Normalization to a common baseline (2016=100) reveals the truth:** Both categories grew at similar rates (~25%), but raw values create an optical illusion of extreme disparity.

---

## 📈 Visualizations

This project includes five publication-quality charts:

1. **Component Breakdown**: All five inflation categories plotted against official CPI baseline
2. **Student vs. National Comparison**: SPI vs. CPI with shaded "inflation gap" area
3. **The Scale Fallacy**: Side-by-side comparison of raw (misleading) vs. normalized (accurate) data
4. **Regional Triple Comparison**: National, Boston, and Student indices on one chart
5. **Summary Dashboard**: Final index values with percentage changes

---

## 💻 Technical Skills Demonstrated

- **API Integration**: Live data retrieval from Federal Reserve Economic Data (FRED)
- **Data Engineering**: Cleaning, filtering, and normalizing time-series data with heterogeneous base years
- **Statistical Methods**: Index theory, Laspeyres weighting, and compositional analysis
- **Data Visualization**: Multi-line plots, area fills, annotations, and comparative charting with Matplotlib
- **Economic Theory**: Applied knowledge of CPI construction, purchasing power parity, and inflation measurement
- **Python Programming**: Pandas DataFrames, custom functions, loops, and time-series manipulation
- **Data Literacy**: Identifying and exposing misleading visualization techniques

---

## 🚀 Tools & Technologies

- **Python 3.x**: Core programming language
- **Pandas**: Time-series data manipulation and analysis
- **Matplotlib**: Statistical visualization and publication-quality charts
- **fredapi**: Federal Reserve Economic Data API client
- **Google Colab**: Cloud-based Jupyter notebook environment

---

## 📂 Project Structure

```
Assignment-1/
│
├── Econ_3916_Assignment_1.ipynb    # Main analysis notebook
├── README.md                        # This file
└── econ_3916_assignment_1.py       # Exported Python script
```

---

## 🎓 Academic Context

**Course**: ECON 3916 - Statistical & Machine Learning for Economics  
**Institution**: Northeastern University  
**Module**: Data Foundations — From Anecdote to Evidence  
**Focus**: Transitioning from consumer of statistics to producer of metrics

---

## 💡 Key Takeaways

1. **National averages hide demographic disparities**: A single CPI cannot capture the diverse economic experiences of students, retirees, urban vs. rural populations, or different income brackets.

2. **Basket composition matters**: The official CPI allocates ~34% to housing, but students may spend 70% on tuition and rent combined—drastically altering effective inflation rates.

3. **Normalization is an ethical imperative**: Comparing raw index values with different base years is not just technically wrong; it's a form of statistical manipulation that can distort public understanding of economic conditions.

4. **Regional disparities compound demographic effects**: Students in high-cost cities like Boston face multiplicative inflation burdens that policy discussions often overlook.

5. **Data literacy is a civic responsibility**: In an era of "alternative facts," the ability to construct, validate, and critique economic metrics is essential for informed citizenship.

---

## 🔗 Repository

**GitHub**: [Link to your repository]  
**Live Notebook**: [Link to your Google Colab]
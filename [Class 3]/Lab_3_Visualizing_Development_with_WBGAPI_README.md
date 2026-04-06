# Visualizing Development with WBGAPI  
**Benchmarking India's Economic Growth (2000-2023)**

## Objective

This project applies the "comparative mindset" to economic data visualization by analyzing India's economic performance against global benchmarks. Using live data from the World Bank API, the goal is to demonstrate how isolated trends can create misleading narratives—what appears as impressive growth in isolation may reveal structural challenges when properly contextualized against peer economies and world averages.

The core question: *Does India's upward-trending GDP signal true convergence with developed economies, or does benchmarking reveal a more complex reality?*

## Methodology

**Data Ingestion (World Bank API):**  
- Retrieved 12 macroeconomic indicators for India (IND), Upper Middle Income countries (UMC), and World (WLD) averages spanning 2000-2023
- Key indicators include:
  - GDP Per Capita (constant 2015 USD) for standard of living comparisons
  - Labor market metrics (participation rate, unemployment)
  - Inflation (CPI) for monetary stability assessment
  - Fiscal indicators (tax revenue, government expenditure)
  - Trade balance (exports, imports)
  - Capital formation (savings, investment)

**Data Transformation:**  
- Cleaned and pivoted World Bank's multi-index structure into analysis-ready format
- Extracted India-specific subset for detailed calculations
- Computed derived metrics:
  - Natural rate of unemployment (5-year moving average)
  - Labor productivity (GDP per worker)
  - Net capital outflow (exports minus imports)
  - Budget balance (tax revenue minus government spending)

**Visualization Strategy:**  
- **Phase 1:** Isolated trend analysis (the "narrow view")
- **Phase 2:** Benchmarked comparison (the "full picture")
- **Phase 3:** Multi-dimensional dashboard synthesis

## Key Findings — *Growth in Context*

**The Illusion of Isolation:**  
When plotted alone, India's GDP per capita shows substantial growth from 2000-2023, creating an impression of rapid development. However, benchmarking against Upper Middle Income countries reveals India remains significantly below its peer group average, with the gap widening in recent years rather than converging.

**Labor Market Dynamics:**  
India's labor force participation rate declined over the study period despite GDP growth, suggesting structural employment challenges not visible in aggregate output measures. Unemployment rates remained persistently elevated compared to global benchmarks.

**Fiscal and Trade Imbalances:**  
- Persistent trade deficits (imports consistently exceeding exports) indicate structural dependence on foreign capital
- Fiscal balance shows chronic government spending exceeding tax revenue, raising questions about long-term sustainability
- Domestic savings rates, while high, have not fully translated into productive investment

**The Comparative Verdict:**  
While India's absolute economic growth is undeniable, relative performance against peer economies reveals slower convergence than headline numbers suggest. True development assessment requires benchmarking—isolated trends can mislead policymakers and investors into overestimating progress.

---

## Technical Implementation

**Tools Used:**
- `wbgapi`: World Bank API client for data retrieval
- `pandas`: Data manipulation and time-series analysis
- `matplotlib` & `seaborn`: Visualization and statistical graphics
- `numpy`: Numerical computations

**Key Techniques:**
- Multi-index DataFrame manipulation
- Rolling window calculations for smoothed trends
- Comparative visualization (isolated vs. benchmarked)
- Executive dashboard design with subplot composition

---

## Project Structure

```
📁 India_WBGAPI_Analysis/
├── 📄 India_Economic_Dashboard.ipynb    # Main analysis notebook
├── 📄 README.md                         # This file
└── 📁 visualizations/                   # Exported charts
    ├── gdp_benchmark.png
    ├── labor_market.png
    ├── trade_balance.png
    └── executive_dashboard.png
```

---

## Skills Demonstrated

- **Economic Theory Application**: Applying growth theory, labor economics, and macroeconomic frameworks to real-world data
- **API Integration**: Live data retrieval and authentication with external databases
- **Data Engineering**: Cleaning, transforming, and structuring multi-dimensional economic data
- **Statistical Analysis**: Computing derived metrics and interpreting time-series patterns
- **Data Visualization**: Creating publication-quality charts that communicate complex economic relationships
- **Critical Thinking**: Recognizing how presentation choices (isolated vs. benchmarked) alter narrative interpretation

---

## Lessons in Data Literacy

This project emphasizes two critical principles:

1. **Context is King**: Absolute growth means little without relative comparison to peer groups
2. **Visualization Ethics**: Chart design choices (axis truncation, isolated plotting, pie charts for rates) can distort truth

The "Ugly" and "Bad" charts demonstrate common manipulation techniques—educating viewers to recognize misleading data presentation in media and policy documents.

---

*This project is part of ECON 3916: Statistical & Machine Learning for Economics, demonstrating the integration of economic theory with modern data science workflows.*
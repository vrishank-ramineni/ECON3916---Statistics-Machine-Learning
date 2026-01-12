# 🍔 Global Purchasing Power Parity Analysis via the Big Mac Index

## 📋 Project Overview

**Objective:** This project applies "Burgernomics" to empirically test the Law of One Price by examining global Big Mac prices as a proxy for purchasing power parity across international currencies.

---

## 🎯 Economic Context

The **Law of One Price** posits that in efficient markets with no transaction costs or trade barriers, identical goods should sell for the same price across countries when expressed in a common currency. The **Big Mac Index**, developed by *The Economist*, serves as a lighthearted yet economically insightful metric to test this theory using McDonald's Big Mac as a standardized global commodity.

This analysis leverages 2015 Big Mac pricing data to calculate implied exchange rates and identify currency misalignments relative to the US Dollar.

---

## 🔬 Methodology

**Data Collection & Processing:**
- Manually constructed a structured dataset using Python dictionaries containing Big Mac prices across multiple countries
- Collected local currency prices and official exchange rates from *The Economist's* 2015 Big Mac Index publication
- Organized data for cross-country comparative analysis

**PPP Calculation:**
- Calculated **Implied PPP Exchange Rates** by dividing each country's Big Mac price by the US Big Mac price
- Compared implied rates against actual market exchange rates to identify deviations from theoretical parity

**Valuation Analysis:**
- Computed percentage over/undervaluation of each currency relative to the USD
- Formula: `((Implied PPP - Actual Rate) / Actual Rate) × 100`
- Positive values indicate overvaluation; negative values indicate undervaluation

**Technical Implementation:**
- Utilized Python and Pandas for data manipulation and calculations
- Applied structured data engineering practices to ensure reproducibility

---

## 📊 Key Findings

*[Insert your specific results here. Example format below:]*

**Currency Valuations Against USD:**
- **Norwegian Krone (NOK)**: Overvalued by X% (Implied PPP: Y, Actual Rate: Z)
- **Chinese Yuan (CNY)**: Undervalued by X% (Implied PPP: Y, Actual Rate: Z)
- **Euro (EUR)**: [Overvalued/Undervalued] by X%

**Economic Implications:**
- Significant deviations from PPP suggest the presence of trade barriers, transportation costs, or local market factors affecting pricing
- Undervalued currencies may indicate potential arbitrage opportunities or lower relative purchasing power
- Overvalued currencies reflect higher cost of living or stronger domestic demand conditions

**Limitations:**
- The Big Mac may not be a perfect proxy due to varying input costs (labor, rent, ingredients) across countries
- Non-tradable components (services, real estate) create natural deviations from PPP
- Analysis assumes perfect substitutability and ignores taste preferences or quality differences

---

## 💡 Skills Demonstrated

- **Economic Theory Application**: Practical implementation of purchasing power parity concepts
- **Data Engineering**: Manual dataset construction and validation
- **Quantitative Analysis**: Currency valuation calculations and comparative metrics
- **Python Programming**: Data manipulation using Pandas library
- **Critical Thinking**: Interpreting results within broader economic context

---

## 🔗 Related Concepts

- Law of One Price
- Purchasing Power Parity (PPP)
- Real vs. Nominal Exchange Rates
- Arbitrage and Market Efficiency
- International Economics

---

*This project demonstrates the application of foundational economic theory to real-world data, bridging theoretical concepts with empirical analysis.*
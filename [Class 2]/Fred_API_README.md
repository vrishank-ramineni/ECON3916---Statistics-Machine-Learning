# The Illusion of Growth & the Composition Effect  
**Deflating History with FRED**

## Objective
This project analyzes long-term U.S. wage trends by correcting nominal wage data for inflation and labor-market composition effects. Using live data from the Federal Reserve Economic Data (FRED) API, the goal is to test whether apparent wage growth reflects real increases in purchasing power or is driven by statistical distortions—particularly during economic shocks such as the COVID-19 pandemic.

## Methodology
- **Data Ingestion (FRED API):**  
  Pulled time-series data directly from FRED using `fredapi`, including:
  - Average Hourly Earnings (AHETPI) for nominal wage trends  
  - Consumer Price Index (CPI) to deflate nominal wages into real wages  

- **Real Wage Construction:**  
  Adjusted nominal wages for inflation to compute real wages, enabling a consistent comparison of purchasing power over time.

- **Anomaly Detection (2020 Pandemic Spike):**  
  Identified a sharp increase in nominal and real wages during 2020 that conflicted with underlying labor-market conditions.

- **Composition Effect Correction:**  
  Retrieved the Employment Cost Index (ECI), a composition-adjusted wage measure, to control for workforce mix changes. This step isolates true wage pressure from artificial increases caused by low-wage workers exiting employment during the pandemic.

## Key Findings — *The Pandemic Paradox*
- **The Money Illusion:**  
  Despite steady nominal wage growth over the past 50 years, real wages remain largely flat once inflation is accounted for, highlighting a persistent disconnect between headline wage growth and actual purchasing power.

- **The Pandemic Paradox:**  
  The apparent wage “boom” in 2020 was not driven by increased labor demand or productivity gains. Instead, it was a statistical artifact caused by the temporary exit of lower-wage workers from the labor force.  
  The composition-adjusted ECI confirms that underlying wage growth remained muted, disproving the narrative of a true pandemic-era wage surge.

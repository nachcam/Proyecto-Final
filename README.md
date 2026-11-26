# The Engel Curve in Mexico: A Descriptive Analysis of Food Expenditure Shares and the Implications of a Food VAT

**Author:** Ignacio Rafael Camacho Mier y Terán
**Course:** Probability and Statistics - Doctorate in Public Policy (DPP26)
**Institution:** Tecnológico de Monterrey

## 1. Research Question and Estimand
This project estimates the Conditional Expectation Function (CEF) of the household food expenditure share on household income to quantify the vulnerability of Mexican households to food price shocks and evaluate the potential regressive impact of a Value-Added Tax (VAT) on basic food. 
The primary estimand is the semi-elasticity of the food share with respect to income per capita (β1). The secondary estimand is the difference in these semi-elasticities between rural and urban households (β3).

## 2. Data Source
The analysis uses microdata from the **2024 National Survey of Household Income and Expenditure (ENIGH)**, published by INEGI. The main dataset used is `concentradohogar.csv`. 

*Note: The raw CSV files are not included in this repository due to GitHub file size limits. To reproduce this analysis, download the "Concentrado Hogar" (CSV format) from the official INEGI website here: [ENIGH 2024 Microdata](https://www.inegi.org.mx/programas/enigh/nc/2024/#microdatos). Once downloaded, place the file in a folder named `data/raw/` before running the scripts.*

## 3. Repository Structure and Reproducibility
To reproduce the results, the scripts must be run in the following order from the root directory (`Proyecto Final`):

1. **`Script/01_load.py`**: Loads the raw data, cleans the variables, creates the rural dummy and the interaction term, and saves a processed dataset (`enigh_analysis.csv`).
2. **`Script/02_plot.py`**: Generates the weighted binscatter plot (Figure 1) using Weighted Least Squares (WLS) to visually diagnose the linearity of the CEF.
3. **`Script/03_regression_analysis.py`**: Estimates the main WLS regression with standard errors clustered at the Primary Sampling Unit (UPM) level and nested within survey strata.
4. **`Script/04_bootstrap.py`**: Runs a cluster bootstrap (500 iterations) to calculate the 95% confidence interval for the urban/rural interaction term.
5. **`Script/05_robustness.py`**: Runs a robustness check using a stricter food definition (excluding restaurant food and beverages) to address measurement biases.
6. **`Script/06_deciles.py`**: Simulates the fiscal incidence of a 16% VAT by income decile to quantify the regressive impact on household budgets.

## 4. Main Findings
*   **Engel's Law holds:** A 1% increase in income per capita is associated with a decrease of approximately 0.09 percentage points in the overall food expenditure share.
*   **Robustness and Regional Differences:** When restricting the food basket to solid items consumed at home, the income effect strengthens (-0.11), and the urban-rural difference becomes statistically significant. Urban households exhibit a more negative income semi-elasticity than rural ones.
*   **Policy Implications (Fiscal Incidence):** A simulated 16% VAT on basic groceries would impose a budget shock of 7.16% on the poorest rural households, compared to just 3.12% on the richest rural households and 2.90% on the richest urban households. The tax is systematically more burdensome for rural areas at every income level, justifying the need for targeted cash transfers.

## 5. Final Report
The complete final report (including the response to the referee) is available in the repository as `Final Project Probability Draft Engel's Law 26NOV26.pdf`.
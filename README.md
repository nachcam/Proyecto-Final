# The Engel Curve in Mexico: A Descriptive Analysis of Food Expenditure Shares and the Implications of a Food VAT

**Author:** Ignacio Rafael Camacho Mier y Terán
**Course:** Probability and Statistics - PhD in Public Policy 
**Institution:** Tecnológico de Monterrey

## 1. Research Question and Estimand
This project estimates the Conditional Expectation Function (CEF) of the food expenditure share on household income to quantify the vulnerability of Mexican households to food price shocks. 
The primary estimand is the semi-elasticity of the food share with respect to income per capita (β1). The secondary estimand is the difference in these semi-elasticities between rural and urban households (β3).

## 2. Data Source
The analysis uses microdata from the **2024 National Survey of Household Income and Expenditure (ENIGH)**, published by INEGI. The main dataset used is `concentradohogar.csv`. 
*Note: The raw CSV files are not included in this repository due to size limits, but they can be downloaded directly from the INEGI website at https://www.inegi.org.mx/programas/enigh/nc/2024/#microdatos.*

## 3. Repository Structure and Reproducibility
To reproduce the results, the scripts must be run in the following order from the root directory (`Proyecto Final`):

1. **`Script/01_load.py`**: Loads the raw data, cleans the variables, creates the rural dummy and the interaction term, and saves a processed dataset (`enigh_analysis.csv`).
2. **`Script/02_plot.py`**: Generates the binscatter plot (Figure 1) to visually diagnose the linearity of the CEF.
3. **`Script/03_regression.py`**: Estimates the main Weighted Least Squares (WLS) regression with standard errors clustered at the Primary Sampling Unit (UPM) level.
4. **`Script/04_bootstrap.py`**: Runs a cluster bootstrap (500 iterations) to calculate the 95% confidence interval for the urban/rural interaction term.

## 4. Main Findings
*   **Engel's Law holds:** A 1% increase in income per capita is associated with a decrease of approximately 0.09 percentage points in the food expenditure share.
*   **No urban/rural difference:** The cluster bootstrap 95% CI for the interaction term is [-0.0013, 0.0086], which includes zero. Therefore, there is no statistically significant evidence that the income semi-elasticity differs between rural and urban areas.
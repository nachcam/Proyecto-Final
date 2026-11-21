import pandas as pd
import statsmodels.formula.api as smf
from pathlib import Path
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

# Define paths and load the processed data
data_path = Path(__file__).parent.parent / "data"
processed_path = data_path / "processed"

print("Loading processed data...")
df_analysis = pd.read_csv(processed_path / "enigh_analysis.csv")

# 2. Define the regression formula (CEF)
formula = "food_share ~ log_income_pc + rural + log_income_pc_rural + tot_integ + menores + edad_jefe + female_head"

# 3. Estimate the model (WLS with scaled weights)
print("\nEstimating OLS regression with clustered standard errors...")
model = smf.wls(formula=formula, data=df_analysis, weights=df_analysis['factor_scaled'])
results = model.fit(cov_type='cluster', cov_kwds={'groups': df_analysis['upm']})

# 4. Print the results as text
print("\n REGRESSION RESULTS")
print(results.summary().tables[1])
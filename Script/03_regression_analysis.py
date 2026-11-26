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

# Define the regression formula (CEF)
formula = "food_share ~ log_income_pc + rural + log_income_pc_rural + tot_integ + menores + edad_jefe + female_head"

# Estimate the model (WLS with scaled weights)
print("\nEstimating OLS regression with clustered standard errors...")
model = smf.wls(formula=formula, data=df_analysis, weights=df_analysis['factor_scaled'])
df_analysis['cluster_var'] = df_analysis['upm'].astype(str) + "_" + df_analysis['est_dis'].astype(str)
results = model.fit(cov_type='cluster', cov_kwds={'groups': df_analysis['cluster_var']})

# Print the results as text
print("\n REGRESSION RESULTS")
print(results.summary().tables[1])
print(f"\nR-squared: {results.rsquared:.4f}")
print(f"\nNumber of observations: {int(results.nobs)}")
print(f"\nNumber of UPMs: {int(df_analysis['upm'].nunique())}")
print("Number of strata:", df_analysis['est_dis'].nunique())

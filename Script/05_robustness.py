import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# Load the data
data_path = Path(__file__).parent.parent / "data" / "processed"
df = pd.read_csv(data_path / "enigh_analysis.csv")

print("Running robustness check with strict food definition...")

# Create the new numerator (restricted)
# Use .clip(lower=0) just in case any household has negative values by error
df['food_share_strict'] = (df['ali_dentro'] - df['bebidas']).clip(lower=0) / df['gasto_mon']

# Define the same formula but with the new dependent variable
formula = "food_share_strict ~ log_income_pc + rural + log_income_pc_rural + tot_integ + menores + edad_jefe + female_head"

# Run the model
model = smf.wls(formula=formula, data=df, weights=df['factor_scaled'])
df['cluster_var'] = df['upm'].astype(str) + "_" + df['est_dis'].astype(str)
results = model.fit(cov_type='cluster', cov_kwds={'groups': df['cluster_var']})

# Print results
print("\n--- ROBUSTNESS RESULTS (Strict Food Share) ---")
print(results.summary().tables[1])
print(f"\nR-squared: {results.rsquared:.4f}")
print(f"\nNumber of observations: {int(results.nobs)}")
print(f"\nNumber of UPMs: {int(df['upm'].nunique())}")
print("Number of strata:", df['est_dis'].nunique())
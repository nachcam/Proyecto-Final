import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import statsmodels.formula.api as smf
import time

warnings.filterwarnings("ignore")

# Load Data
data_path = Path(__file__).parent.parent / "data"
processed_path = data_path / "processed"
df = pd.read_csv(processed_path / "enigh_analysis.csv")

print("Starting the optimized bootstrap procedure...")
start_time = time.time()
n_iterations = 500
bootstrap_results = []
upms = df['upm'].unique()
formula = "food_share ~ log_income_pc + rural + log_income_pc_rural + tot_integ + menores + edad_jefe + female_head"

# Run Bootstrap
np.random.seed(42)
for i in range(n_iterations):
    sampled_upms = np.random.choice(upms, size=len(upms), replace=True)
    upm_counts = pd.Series(sampled_upms).value_counts()
    boot_weights = df['upm'].map(upm_counts).fillna(0).values
    final_weights = df['factor_scaled'].values * boot_weights
    
    valid_idx = boot_weights > 0
    sample_df = df[valid_idx].copy()
    sample_weights = final_weights[valid_idx]
    
    model = smf.wls(formula=formula, data=sample_df, weights=sample_weights)
    results = model.fit(cov_type='cluster', cov_kwds={'groups': sample_df['upm']})
    
    bootstrap_results.append(results.params["log_income_pc_rural"])
    
    if (i + 1) % 50 == 0:
        print(".", end="", flush=True)

# Results
print("Bootstrap completed, 500 interations.")
lower_bound = np.percentile(bootstrap_results, 2.5)
upper_bound = np.percentile(bootstrap_results, 97.5)

print(f'The 95% confidence interval for log_income_pc_rural is: [{lower_bound:.4f}, {upper_bound:.4f}]')
print(f'Time taken {time.time() - start_time:.2f} seconds.')
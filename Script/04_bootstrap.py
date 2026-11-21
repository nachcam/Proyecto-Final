import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import statsmodels.formula.api as smf
import time

# Ignore warnings
warnings.filterwarnings("ignore")

# Load the data
data_path = Path(__file__).parent.parent / "data"
processed_path = data_path / "processed"
df = pd.read_csv(processed_path / "enigh_analysis.csv")

# Starting with the Booststrap procedure
print("Starting the bootstrap procedure...")
start_time = time.time()
n_iterations = 500
bootstrap_results = []
upms = df['upm'].unique()
formula = "food_share ~ log_income_pc + rural + log_income_pc_rural + tot_integ + menores + edad_jefe + female_head"

for i in range(n_iterations):
    # Resample UPMs with replacement
    sampled_upms = np.random.choice(upms, size=len(upms), replace=True)
    
    # Create a new DataFrame for the bootstrap sample
    bootstrap_sample = pd.concat([df[df['upm'] == upm] for upm in sampled_upms])
    
    # Fit the model on the bootstrap sample
    model = smf.wls(formula=formula, data=bootstrap_sample, weights=bootstrap_sample['factor_scaled'])
    results = model.fit(cov_type='cluster', cov_kwds={'groups': bootstrap_sample['upm']})
    
    # Store the coefficients
    bootstrap_results.append(results.params["log_income_pc_rural"])

    # Now let's find the bounds for the 95% confidence interval
    lower_bound = np.percentile(bootstrap_results, 2.5)
    upper_bound = np.percentile(bootstrap_results, 97.5)

    # Print the results for this iteration
    print("Boostrap results")
    print(f'The 95% confidence interval for the coefficient of log_income_pc_rural is: [{lower_bound:.4f}, {upper_bound:.4f}]')
    print(f'If this interval does not include zero, we can reject the null hypothesis that the coefficient is zero at the 5% significance level.')
    print(f'Time taken {time.time() - start_time:.2f} seconds.')


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# Load Data 
data_path = Path(__file__).parent.parent / "data" / "processed"
df = pd.read_csv(data_path / "enigh_analysis.csv")

print("Creating Weighted Binscatter plot...")

# Create Bins 
df['income_bin'] = pd.qcut(df['log_income_pc'], q=20, duplicates='drop')

# Calculate Weighted Averages
def weighted_average(group):
    return pd.Series({
        'log_income_pc': np.average(group['log_income_pc'], weights=group['factor_scaled']),
        'food_share': np.average(group['food_share'], weights=group['factor_scaled'])
    })

binscatter_data = df.groupby('income_bin', observed=True).apply(weighted_average).reset_index()

# Generate the plot
plt.figure(figsize=(10, 6))
plt.scatter(binscatter_data['log_income_pc'], binscatter_data['food_share'], 
            color='blue', label='Weighted Bin averages (20 bins)', s=50, zorder=3, alpha=0.7)

# Weighted Linear Trend (WLS)
trend_model = smf.wls("food_share ~ log_income_pc", data=df, weights=df['factor_scaled']).fit()
x_vals = np.linspace(binscatter_data['log_income_pc'].min(), binscatter_data['log_income_pc'].max(), 100)
y_vals = trend_model.params['Intercept'] + trend_model.params['log_income_pc'] * x_vals

plt.plot(x_vals, y_vals, color='red', linestyle='--', label='Weighted Linear fit (WLS)', zorder=2)

plt.title('Weighted Binscatter: Food Share vs Log Income per Capita', fontsize=14)
plt.xlabel('Log Income per Capita', fontsize=12)
plt.ylabel('Food Share (Proportion)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3, zorder=1)

# Save and show the plot
output_path = data_path / "binscatter_weighted.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Plot saved to: {output_path}")
plt.show()
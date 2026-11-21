import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

# Define paths and load the processed data
data_path = Path(__file__).parent.parent / "data"
processed_path = data_path / "processed"
df = pd.read_csv(processed_path / "enigh_analysis.csv")

# Create 20 quantile bins for log_income_pc
df['income_quantile'] = pd.qcut(df['log_income_pc'], 20, labels=False)
binscatter_data = df.groupby('income_quantile').agg({"log_income_pc": "mean", "food_share": "mean"}).reset_index()

# Create the binscatter plot
plt.figure(figsize=(10, 6))
plt.scatter(binscatter_data['log_income_pc'], binscatter_data['food_share'], color='blue', label = "Bin averages (20 bins)", s=50,zorder=3, alpha=0.7)

# Fit a linear regression line to the binned data
z = np.polyfit(binscatter_data['log_income_pc'], binscatter_data['food_share'], 1)
p = np.poly1d(z)
plt.plot(binscatter_data['log_income_pc'], p(binscatter_data['log_income_pc']), color='red', linestyle = "--", label='Linear fit', zorder=2)

# Add labels and title
plt.title('Binscatter Plot: Food Share vs Log Income per Capita')
plt.xlabel('Log Income per Capita')
plt.ylabel('Food Share')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.3, zorder=1)

# Save the plot
output_file = processed_path / "binscatter_plot.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()

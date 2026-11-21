import pandas as pd
import numpy as np
from pathlib import Path
import warnings

# Ignore warnings
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Define paths
data_path = Path(__file__).parent.parent / "data"
raw_data_path = data_path / "raw"
processed_path = data_path / "processed"

# Create processed folder. 
processed_path.mkdir(exist_ok=True)

# Load the raw data
print("Loading raw data...")
df_conc = pd.read_csv(raw_data_path / "concentradohogar.csv", dtype={"foliohog": str, "folioviv": str}, low_memory=False)

# Let's clean the data and prepare it for regression analysis
print("Processing data...")
df = df_conc.copy()

# Create rural dummy (1 if tam_loc == 4, which means < 2,500 inhabitants)
df["rural"] = (df["tam_loc"] == 4).astype(int)

# Calculate Food Share 
df['food_share'] = df['alimentos'] / df['gasto_mon']

# Calculate income per capita
df['income_pc'] = df['ing_cor'] / df['tot_integ']

# Create log income (replace 0 with NaN to avoid errors)
df['log_income_pc'] = np.log(df['income_pc'].replace(0, np.nan))

# Create the interaction term
df['log_income_pc_rural'] = df['log_income_pc'] * df['rural']

# Drop missing values in key variables
df_analysis = df.dropna(subset=['food_share', 'log_income_pc', 'edad_jefe', 'sexo_jefe']).copy()

# Create dummy for female head of household (1 = Female, 0 = Male)
df_analysis['female_head'] = (df_analysis['sexo_jefe'] == 2).astype(int)

# Scale the weights (prevent memory issues in statsmodels)
df_analysis['factor_scaled'] = df_analysis['factor'] / df_analysis['factor'].mean()

# Save the final dataset
output_file = processed_path / "enigh_analysis.csv"
df_analysis.to_csv(output_file, index=False)

print(f"Data processed successfully. Final sample size: {df_analysis.shape[0]} households.")
print(f"Saved to: {output_file}")
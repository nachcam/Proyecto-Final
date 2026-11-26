import pandas as pd
import numpy as np
from pathlib import Path

# Load the processed data
data_path = Path(__file__).parent.parent / "data" / "processed"
df = pd.read_csv(data_path / "enigh_analysis.csv")

print("Calculating decile analysis for restricted food share...\n")

# Create the restricted food share variable
df['restricted_food_share'] = (df['ali_dentro'] - df['bebidas']).clip(lower=0) / df['gasto_mon']

# Create income deciles
df['income_decile'] = pd.qcut(df['income_pc'], q=10, labels=False) + 1

# Group by decile and calculate the average restricted food share for urban and rural households
decile_table = df.groupby('income_decile').apply(
    lambda x: pd.Series({
        'Urban_Share': x[x['rural'] == 0]['restricted_food_share'].mean(),
        'Rural_Share': x[x['rural'] == 1]['restricted_food_share'].mean()
    })
).reset_index()

# Calculate the impact of a 16% VAT on food for each decile
decile_table['Urban_VAT_Impact'] = decile_table['Urban_Share'] * 0.16
decile_table['Rural_VAT_Impact'] = decile_table['Rural_Share'] * 0.16

# Format the table for display
decile_table_display = decile_table.copy()
cols_to_pct = ['Urban_Share', 'Rural_Share', 'Urban_VAT_Impact', 'Rural_VAT_Impact']
decile_table_display[cols_to_pct] = decile_table_display[cols_to_pct] * 100

print(decile_table_display.round(2).to_string(index=False))

# Save the decile analysis table to a CSV file
decile_table_display.to_csv(data_path / "decile_analysis.csv", index=False)
print("\nTable saved to decile_analysis.csv")
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.25.2",
#     "numpy>=2.5.5",
#     "pandas>=3.1.1",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Final Project: Engel's Law in Mexico
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's firt load the data set
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    from pathlib import Path
    import warnings

    warnings.filterwarnings("ignore")

    # Paths
    data_path = Path(__file__).parent.parent / "data"
    raw_data_path = data_path / "raw"
    processed_path = data_path / "processed"
    processed_path.mkdir(exist_ok=True)

    # Loading the data
    df_conc = pd.read_csv(raw_data_path / "concentradohogar.csv", dtype={"foliohog": str, "folioviv": str}, low_memory=False)

    # Show summary of the loaded data
    mo.md(f"### ¡Loaded!\n- Concentrado: {df_conc.shape[0]}")

    return df_conc, mo, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's begin to process the data
    """)
    return


@app.cell
def _(df_conc, np):
    # Is the "Concetrado" data set divided only by urban/rural?
    print("Unique values in tam_loc:", df_conc['tam_loc'].unique())

    # No, it' devided in 4 categories, let's define a rural dummy
    # Let's make a copy of the original dataframe
    df = df_conc.copy()

    # Now create the rural dummy
    df["rural"] = (df_conc["tam_loc"] == 4).astype(int)

    # Let's create the variables of interest for the analysis
    df["food share"] = df["alimentos"] / df["gasto_mon"]
    df["income_pc"] = df["ing_cor"] / df["tot_integ"]
    df["log_income_pc"] = np.log(df["income_pc"].replace(0, np.nan))  # Replace 0 with NaN to avoid log(0)

    # Now let's create the interaction term
    df["log_income_pc_rural"] = df["log_income_pc"] * df["rural"]

    # Let's clean the data set by dropping rows with NaN values in the variables of interest
    df_analysis = df.dropna(subset=["food share", "log_income_pc", "edad_jefe", "sexo_jefe"])

    # Now let's focus on the control variables and create a dummy for female heads of households
    df_analysis["female_head"] = (df_analysis["sexo_jefe"] == 2).astype(int)

    # Now let's compare out data set with the original data set to see how many observations we lost
    print(f"Original data set size: {df.shape[0]} rows")
    print(f"Analysis data set size: {df_analysis.shape[0]} rows")  

    # Now let's quickly analyze our variables
    df_analysis[["food share", "log_income_pc", "edad_jefe", "female_head"]].describe().round(2).transpose()  

    return (df_analysis,)


@app.cell
def _(df_analysis):
    # Let's import statsmodels for the regression analysis
    import statsmodels.formula.api as smf

    # Marimo's memory is collapsing with the actual weights, so let's scale them
    df_analysis["factor_scaled"] = df_analysis["factor"] / df_analysis["factor"].mean()

    # Now let's write our regression model using the formula API
    formula = "food_share ~ log_income_pc + rural +log_income_pc_rural + tot_integ + menores + edad_jefe + female_head"

    # Let's fit the model
    model = smf.wls(formula=formula, data=df_analysis, weights= df_analysis['factor_scaled']).fit()

    # Let's now cluster the standard errors by UPM
    results = model.fit(cov_type='cluster', cov_kwds={'groups': df_analysis['upm']})

    # Now let's print the summary of the regression analysis
    results_df = results.summary2().tables[1]
    print(results_df.round(4).to_string())
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

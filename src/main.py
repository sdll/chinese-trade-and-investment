# %% [markdown]
# # Imports
# %%
from IPython.display import display, Markdown, Latex
from matplotlib import rcParams
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

# %% [markdown]
# # Configuration

# %%
rcParams["figure.figsize"] = 11.7, 8.27
rcParams["figure.dpi"] = 150
# %% [markdown]
# # Utilities
# %%
def read_and_tag(basepath, tag_start, delimiter="-", skiprows=2):
    files = glob.glob(basepath + "*.csv")
    dataframes = []
    for filename in files:
        tag = " ".join(
            map(
                lambda word: word.capitalize(),
                os.path.splitext(os.path.basename(filename))[0].split(delimiter)[
                    tag_start:
                ],
            )
        )
        df = pd.read_csv(filename, skiprows=skiprows, encoding="ISO-8859-1")
        df["Type"] = tag
        dataframes.append(df)
    return pd.concat(dataframes, axis=0, ignore_index=True)


# %% [markdown]
# # Data
# %%

df_fdi_inward_flow = pd.read_csv(
    "./src/data/foreign-direct-investment-inward-flow.csv", skiprows=4
)
df_fdi_outward_flow = pd.read_csv(
    "./src/data/foreign-direct-investment-outward-flow.csv", skiprows=4
)
df_fdi_inward_stock = pd.read_csv(
    "./src/data/foreign-direct-investment-inward-stock.csv", skiprows=4
)
df_fdi_outward_stock = pd.read_csv(
    "./src/data/foreign-direct-investment-outward-stock.csv", skiprows=4
)

import_data_basepath = os.path.join("./src/data/chinese-import-")
export_data_basepath = os.path.join("./src/data/chinese-export-")


df_import = read_and_tag(import_data_basepath, 2)
df_export = read_and_tag(export_data_basepath, 2)


# %% [markdown]
# # Foreign Direct Investment in China, 2013-2017
# %%
inward_fdi_2017_stock = df_fdi_inward_stock.iloc[1, -1]
outward_fdi_2017_stock = df_fdi_outward_stock.iloc[1, -1]

display(
    Markdown(
        f"China received **{inward_fdi_2017_stock:.0f} Million \$ US** in stock inward foreign direct investment, and spent **{outward_fdi_2017_stock:.0f} Million \$** as outward FDI in 2017."
    )
)

# %%
fdi_2017_stock = pd.DataFrame(columns=["Volume", "Type", "Year"])

fdi_2017_stock.loc["Inward", "Volume"] = inward_fdi_2017_stock
fdi_2017_stock.loc["Outward", "Volume"] = outward_fdi_2017_stock
fdi_2017_stock.loc["Outward", "Type"] = "Outward"
fdi_2017_stock.loc["Inward", "Type"] = "Inward"
fdi_2017_stock.loc[:, "Year"] = 2017

plot = sns.barplot(x="Type", y="Volume", data=fdi_2017_stock)
plot.set(xlabel="FDI Type", ylabel="Stock Volume, Million $")

# %%
raw_inward_fdi_2013_2017_flow = df_fdi_inward_flow.iloc[1, -5:]
raw_outward_fdi_2013_2017_flow = df_fdi_outward_flow.iloc[1, -5:]

# %%
display(
    Markdown(
        f"Over the last five years, year-on-year inward FDI flows grew from **{raw_inward_fdi_2013_2017_flow[0]:.0f}** to **{raw_inward_fdi_2013_2017_flow[-1]:.0f} Million \$US** , while the outward foreign direct investment spiked in 2016 at the level of **{raw_outward_fdi_2013_2017_flow[-2]:.0f} Million \$US**, falling to **{raw_outward_fdi_2013_2017_flow[-1]:.0f} Million \$US**, the level of 2014, in 2017"
    )
)


# %%
inward_fdi_2013_2017_flow = pd.DataFrame()
inward_fdi_2013_2017_flow.insert(0, "Flow Volume", raw_inward_fdi_2013_2017_flow)
inward_fdi_2013_2017_flow["Year"] = inward_fdi_2013_2017_flow.index
inward_fdi_2013_2017_flow["Type"] = "Inward"

outward_fdi_2013_2017_flow = pd.DataFrame()
outward_fdi_2013_2017_flow.insert(0, "Flow Volume", raw_outward_fdi_2013_2017_flow)
outward_fdi_2013_2017_flow["Year"] = outward_fdi_2013_2017_flow.index
outward_fdi_2013_2017_flow["Type"] = "Outward"

fdi_2013_2017_flow = pd.concat([inward_fdi_2013_2017_flow, outward_fdi_2013_2017_flow])
fdi_2013_2017_flow = fdi_2013_2017_flow.reset_index(drop=True)
fdi_2013_2017_flow

# %%
plot = sns.pointplot(x="Year", y="Flow Volume", hue="Type", data=fdi_2013_2017_flow)
plot.set(ylabel="Flow Volume, Million $")

# %% [markdown]
# # Chinese Trade, 2013-2017
# ## Trade Dynamics

# %%
years = list(map(lambda year: str(year), range(2013, 2018)))
five_year_import = df_import[df_import.iloc[:, 0] == "World"][
    years + ["Type"]
].reset_index(drop=True)
five_year_import = pd.melt(
    five_year_import,
    id_vars=["Type"],
    var_name="Year",
    value_name="Trade Volume, Thousand $US",
)
five_year_import["Trade Volume, Thousand $US"] = five_year_import[
    "Trade Volume, Thousand $US"
].astype("float")


five_year_export = df_export[df_export.iloc[:, 0] == "World"][
    years + ["Type"]
].reset_index(drop=True)
five_year_export = pd.melt(
    five_year_export,
    id_vars=["Type"],
    var_name="Year",
    value_name="Trade Volume, Thousand $US",
)
five_year_export["Trade Volume, Thousand $US"] = five_year_export[
    "Trade Volume, Thousand $US"
].astype("float")

import_dynamics = five_year_import.groupby(["Year"]).sum()
import_dynamics["Type"] = "Import"
export_dynamics = five_year_export.groupby(["Year"]).sum()
export_dynamics["Type"] = "Export"
trade_dynamics = pd.concat([import_dynamics, export_dynamics])
trade_dynamics["Year"] = trade_dynamics.index

sns.pointplot(x="Year", y="Trade Volume, Thousand $US", hue="Type", data=trade_dynamics)
# %% [markdown]
# ## Import
# %%
# %%
developed_countries_trade_import = df_import[["YEAR", "2017"]][
    df_import["YEAR"].str.contains("Developed economies:")
]
# remove duplicates
developed_countries_trade_import = developed_countries_trade_import.drop(
    developed_countries_trade_import[
        developed_countries_trade_import["YEAR"].str.contains("Asia and Oceania")
    ].index
)
developed_countries_trade_import["2017"] = developed_countries_trade_import[
    "2017"
].astype("float")
developed_countries_trade_import = developed_countries_trade_import.rename(
    columns={"YEAR": "Country Type", "2017": "Merchandise Trade Volume, 1000 $US"}
)
sns.barplot(
    x="Country Type",
    y="Merchandise Trade Volume, 1000 $US",
    data=developed_countries_trade_import,
)

# %%
developing_countries_trade_import = df_import[["YEAR", "2017"]][
    df_import["YEAR"].str.contains("Developing economies:")
]
# remove duplicates
developing_countries_trade_import = developing_countries_trade_import.drop(
    developing_countries_trade_import[
        developing_countries_trade_import["YEAR"].str.contains("Asia and Oceania")
    ].index
)
developing_countries_trade_import["2017"] = developing_countries_trade_import[
    "2017"
].astype("float")
developing_countries_trade_import = developing_countries_trade_import.rename(
    columns={"YEAR": "Country Type", "2017": "Merchandise Trade Volume, 1000 $US"}
)
developing_countries_trade_import_plot = sns.barplot(
    x="Country Type",
    y="Merchandise Trade Volume, 1000 $US",
    data=developing_countries_trade_import,
)
developing_countries_trade_import_plot.set_xticklabels(
    developing_countries_trade_import_plot.get_xticklabels(), rotation=90
)
# %%
import_trade_by_type = df_import[["Type", "2017"]]
import_trade_by_type["2017"] = pd.to_numeric(
    import_trade_by_type["2017"], errors="coerce"
).fillna(0)

import_trade_by_type = import_trade_by_type.groupby("Type").sum()
import_trade_by_type["Type"] = import_trade_by_type.index
import_trade_by_type = import_trade_by_type.rename(
    columns={"2017": "Merchandise Trade Volume, 1000 $US"}
)
import_trade_by_type_plot = sns.barplot(
    x="Type", y="Merchandise Trade Volume, 1000 $US", data=import_trade_by_type
)
import_trade_by_type_plot.set_xticklabels(
    import_trade_by_type_plot.get_xticklabels(), rotation=90
)

# %% [markdown]
# ## Export

# %%
developed_countries_trade_export = df_export[["YEAR", "2017"]][
    df_export["YEAR"].str.contains("Developed economies:")
]
# remove duplicates
developed_countries_trade_export = developed_countries_trade_export.drop(
    developed_countries_trade_export[
        developed_countries_trade_export["YEAR"].str.contains("Asia and Oceania")
    ].index
)
developed_countries_trade_export["2017"] = developed_countries_trade_export[
    "2017"
].astype("float")
developed_countries_trade_export = developed_countries_trade_export.rename(
    columns={"YEAR": "Country Type", "2017": "Merchandise Trade Volume, 1000 $US"}
)
sns.barplot(
    x="Country Type",
    y="Merchandise Trade Volume, 1000 $US",
    data=developed_countries_trade_export,
)

# %%
developing_countries_trade_export = df_export[["YEAR", "2017"]][
    df_export["YEAR"].str.contains("Developing economies:")
]
# remove duplicates
developing_countries_trade_export = developing_countries_trade_export.drop(
    developing_countries_trade_export[
        developing_countries_trade_export["YEAR"].str.contains("Asia and Oceania")
    ].index
)
developing_countries_trade_export["2017"] = developing_countries_trade_export[
    "2017"
].astype("float")
developing_countries_trade_export = developing_countries_trade_export.rename(
    columns={"YEAR": "Country Type", "2017": "Merchandise Trade Volume, 1000 $US"}
)
developing_countries_trade_export_plot = sns.barplot(
    x="Country Type",
    y="Merchandise Trade Volume, 1000 $US",
    data=developing_countries_trade_export,
)
developing_countries_trade_export_plot.set_xticklabels(
    developing_countries_trade_export_plot.get_xticklabels(), rotation=90
)
# %%
export_trade_by_type = df_export[["Type", "2017"]]
export_trade_by_type["2017"] = pd.to_numeric(
    export_trade_by_type["2017"], errors="coerce"
).fillna(0)

export_trade_by_type = export_trade_by_type.groupby("Type").sum()
export_trade_by_type["Type"] = export_trade_by_type.index
export_trade_by_type = export_trade_by_type.rename(
    columns={"2017": "Merchandise Trade Volume, 1000 $US"}
)
export_trade_by_type_plot = sns.barplot(
    x="Type", y="Merchandise Trade Volume, 1000 $US", data=export_trade_by_type
)
export_trade_by_type_plot.set_xticklabels(
    export_trade_by_type_plot.get_xticklabels(), rotation=90
)

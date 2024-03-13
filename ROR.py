import os.path
import math as m
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
plt.style.use("seaborn-v0_8")

# load data and filter by columns of interest

ror_data_raw = pd.read_csv("bnetza_mastr_hydro_raw.csv",
                        index_col = 0, sep=",")

columns = ["Einheittyp","Bruttoleistung","Nettonennleistung","EinheitBetriebsstatus","AnlageBetriebsstatus",
           "Gemeinde","Laengengrad","Breitengrad","ArtDerWasserkraftanlage","ArtDesZuflusses"]

ror_data = ror_data_raw[columns]

# filter dataframe by regions

regions = ["Rüdersdorf bei Berlin", "Strausberg", "Erkner", "Grünheide (Mark)",
           "Kiel", "Ingolstadt", "Kassel", "Bocholt", "Zwickau"]

gemeindeschluessel = {
    "Rüdersdorf bei Berlin": "12064428",
    "Strausberg": "12064472",
    "Erkner": "12067124",
    "Grünheide (Mark)": "12067201",
    "Ingolstadt":"09161000",
    "Kassel": "06611000",
    "Bocholt": "05554008",
    "Kiel": "01002000",
    "Zwickau": "14524330",
}

dfs = []
for region in regions:
    dfs.append(ror_data.loc[ror_data["Gemeinde"] == region])

ror_regions = pd.concat(dfs)

# calculate dispatch data

full_load_hours = 3800 # source: digipipe

ror_grouped = ror_regions.groupby("Gemeinde").Bruttoleistung.sum()

data = {"Bruttoleistung_kW": ror_grouped.values
}
df_ror_disp = pd.DataFrame(data,index=ror_grouped.index)

df_ror_disp["estimated_Generation_MWh"] = df_ror_disp["Bruttoleistung_kW"] * full_load_hours /1e3
df_ror_disp["cf"] = df_ror_disp["estimated_Generation_MWh"].div(df_ror_disp["Bruttoleistung_kW"] * 8760 /1e3)
df_ror_disp["dispatch_kW"] = df_ror_disp["estimated_Generation_MWh"]*1e3 / 8760
df_ror_disp["dispatch_kW_standardize"] = df_ror_disp["dispatch_kW"] / (df_ror_disp["estimated_Generation_MWh"] * 1e3)


global date_range
start_date = "2011-01-01 00:00:00"
end_date = "2011-12-31 23:00:00"
date_range = pd.date_range(start=start_date, end=end_date, freq='H')

ror_timeseries = pd.DataFrame(index=date_range,columns=regions)

for column in ror_timeseries:
    if column in df_ror_disp.index:
        ror_timeseries[column] = df_ror_disp.loc[column,"dispatch_kW_standardize"]

for column in ror_timeseries:
    ror_timeseries.rename(columns={column:gemeindeschluessel[column]}, inplace=True)


ror_timeseries.to_csv("timeseries/ror_feedin_timeseries.csv")
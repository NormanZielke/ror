import os.path
import math as m
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
plt.style.use("seaborn-v0_8")

# load data in filter by columns of interest

ror_data_raw = pd.read_csv("bnetza_mastr_hydro_raw.csv",
                        index_col = 0, sep=",")

columns = ["Einheittyp","Bruttoleistung","Nettonennleistung","EinheitBetriebsstatus","AnlageBetriebsstatus",
           "Gemeinde","Laengengrad","Breitengrad","ArtDerWasserkraftanlage","ArtDesZuflusses"]

ror_data = ror_data_raw[columns]

# filter dataframe by regions

regions = ["Rüdersdorf bei Berlin", "Strausberg", "Erkner", "Grünheide (Mark)",
           "Kiel", "Ingolstadt", "Kassel", "Bocholt", "Zwickau"]

dfs= []
for region in regions:
    dfs.append(ror_data.loc[ror_data["Gemeinde"] == region])

ror_regions = pd.concat(dfs)

# calculate dispatch data

full_load_hours = 3800 # source: digipipe

ror_grouped = ror_regions.groupby("Gemeinde").Bruttoleistung.sum()

data = {"Bruttoleistung_kW": ror_grouped.values
}
df_ror_disp = pd.DataFrame(data,index=ror_grouped.index)

df_ror_disp["estimated_Generation_GWh"] = df_ror_disp["Bruttoleistung"] * full_load_hours /1e3
df_ror_disp["cf"] = df_ror_disp["estimated_Generation_GWh"].div(df_ror_disp["Bruttoleistung"] * 8760 /1e3)
df_ror_disp["dispatch_kW"] = df_ror_disp["estimated_Generation_GWh"]*1e3 / 8760

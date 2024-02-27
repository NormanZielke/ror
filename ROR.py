import os.path
import math as m
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
plt.style.use("seaborn-v0_8")


ror_data = pd.read_csv("bnetza_mastr_hydro_raw.csv",
                        index_col = 0, sep=",", parse_dates= True)

columns = ["Einheittyp","Bruttoleistung","Nettonennleistung","EinheitBetriebsstatus","AnlageBetriebsstatus",
           "Gemeinde","Laengengrad","Breitengrad","ArtDerWasserkraftanlage","ArtDesZuflusses"]

ror_data = ror_data[columns]

regions = ["Rüdersdorf bei Berlin", "Strausberg", "Erkner", "Grünheide (Mark)",
           "Kiel", "Ingolstadt", "Kassel", "Bocholt", "Zwickau"]

dfs= []
for region in regions:
    dfs.append(ror_data.loc[ror_data["Gemeinde"] == region])

ror_regions = pd.concat(dfs)

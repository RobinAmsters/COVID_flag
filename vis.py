#!/usr/bin/env python2
# @brief 
# @author Robin Amsters
# @bug No known bugs

# Data source: https://epistat.wiv-isp.be/covid/

import matplotlib.pyplot as plt
import pandas as pd

# Load data
data = pd.read_excel('data/COVID19BE.xlsx', sheet_name="CASES_AGESEX", index_col="DATE")

# Format data
data = data.dropna() # Drop final nan entries
data = data.groupby(["DATE"]).sum() # Get total number of cases per day, groups municipality, age and sex together
df_cum = data["CASES"].cumsum() # Get cumulative number of cases per day

# Visualization
fig, axs = plt.subplots(2)
data.plot(ax=axs[0], legend=False)
axs[0].set_ylabel("Cases per day")
axs[0].grid()

df_cum.plot(ax = axs[1])
axs[1].set_ylabel("Cumulative cases")
axs[1].grid()

plt.show()
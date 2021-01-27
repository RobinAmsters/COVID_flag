#!/usr/bin/env python2
# @brief 
# @author Robin Amsters
# @bug No known bugs
import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_excel('data/COVID19BE.xlsx', sheet_name="CASES_AGESEX", index_col="DATE")
print(df)
# Format data
df = df.dropna() # Drop final nan entries
df = df.groupby(["DATE"]).sum() # Get cumulative number of cases, groups municipality, age and sex together

# Visualization
df.plot()
plt.ylabel("Cases per day")
plt.grid()
plt.show()
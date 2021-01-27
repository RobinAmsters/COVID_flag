#!/usr/bin/env python2
# @brief 
# @author Robin Amsters
# @bug No known bugs

# Data source: https://epistat.wiv-isp.be/covid/
# Flag image source: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg

# TODO animation per day
# TODO Figure out resolution, maybe make 1 pixel per inhabitant. Alternatively scale the pixels that are removed in proportion to the toal inhabitants

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data
data = pd.read_excel('data/COVID19BE.xlsx', sheet_name="CASES_AGESEX", index_col="DATE") # Load test file with few rows for easier testing for now
flag = cv2.imread("data/Flag_of_Belgium.png")
height, width = flag.shape[:2]

# Format data
data = data.dropna() # Drop final nan entries
data = data.groupby(["DATE"]).sum() # Get total number of cases per day, groups municipality, age and sex together
data_cum = data["CASES"].cumsum() # Get cumulative number of cases per day
total_cases = data_cum[-1] # Total number of cases in Belgium so far

# Remove one pixel for every COVID case
pixels_x = np.random.uniform(0, width, total_cases).astype(int)
pixels_y = np.random.uniform(0, height, total_cases).astype(int)
flag[pixels_y, pixels_x] = (255, 255, 255)

# Line plots of cases
# fig, axs = plt.subplots(2)
# data.plot(ax=axs[0], legend=False)
# axs[0].set_ylabel("Cases per day")
# axs[0].grid()
#
# data_cum.plot(ax = axs[1])
# axs[1].set_ylabel("Cumulative cases")
# axs[1].grid()
#
# plt.show()

cv2.imshow("Flag", flag)
#!/usr/bin/env python2
# @brief 
# @author Robin Amsters
# @bug No known bugs

# Data source: https://epistat.wiv-isp.be/covid/
# Flag image source: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg

# TODO animation per day
# TODO Figure out resolution, maybe make 1 pixel per inhabitant. Alternatively scale the pixels that are removed in proportion to the toal inhabitants

# Idea: start from empty and make a flag of vaccinated ppl

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

inhabitants = 11492641  # https://statbel.fgov.be/nl/themas/bevolking/structuur-van-de-bevolking
scaling = flag.size/total_cases

# Remove one pixel for every COVID case
pixels_x = np.random.uniform(0, width, int(total_cases/scaling)).astype(int)
pixels_y = np.random.uniform(0, height, int(total_cases/scaling)).astype(int)
flag[pixels_y, pixels_x] = (255, 255, 255)

font = cv2.FONT_HERSHEY_SIMPLEX
image = cv2.putText(flag, data_cum.keys()[-1], (0,100), font, 3, (0, 255, 0), 2, cv2.LINE_AA) # Add data to picture
cv2.imshow("Flag", image)
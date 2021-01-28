#!/usr/bin/env python2
# @brief 
# @author Robin Amsters
# @bug No known bugs

# Data source: https://epistat.wiv-isp.be/covid/
# Flag image source: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg

# TODO keep track of pixels that have been removed and only remove additional ones
# TODO remember to process complete file instead of test
# TODO animation per day
# TODO Figure out resolution, maybe make 1 pixel per inhabitant. Alternatively scale the pixels that are removed in proportion to the toal inhabitants

# Idea: start from empty and make a flag of vaccinated ppl
# Idea make it relative to the belgian map

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy

# Parameters
inhabitants = 11492641  # https://statbel.fgov.be/nl/themas/bevolking/structuur-van-de-bevolking
FPS = 1
font = cv2.FONT_HERSHEY_SIMPLEX
dates_to_process = 5 # Number of data entries to process for testing

# Load data
data = pd.read_excel('data/COVID19BE.xlsx', sheet_name="CASES_AGESEX", index_col="DATE") # Load test file with few rows for easier testing for now
flag_orig = cv2.imread("data/Flag_of_Belgium.png")
# flag_orig = cv2.cvtColor(flag_orig, cv2.COLOR_BGR2RGB) # For use in matplotlib
height, width = flag_orig.shape[:2]

# Format data
data = data.dropna() # Drop final nan entries
data = data.groupby(["DATE"]).sum() # Get total number of cases per day, groups municipality, age and sex together
data_cum = data["CASES"].cumsum() # Get cumulative number of cases per day
total_cases = data_cum[-1] # Total number of cases in Belgium so far

# Start video writier
fourcc = cv2.VideoWriter_fourcc(*'MP42')
video = cv2.VideoWriter('results/flag_cases.avi', fourcc, float(FPS), (width, height))


scaling = flag_orig.size/total_cases # Remove pixels relative to population
removed_pixels_x = np.array([], dtype=int) # 10*flag_orig.size*np.ones(2,flag_orig.size) # initialize indexes as large number, to be overrided later
removed_pixels_y = np.array([], dtype=int)
for date in data_cum.keys()[0:dates_to_process]: # Loop over all dates and create frame for every entry
    print("Processing day: " + date)
    flag = copy.deepcopy(flag_orig)

    # Determine which pixels to remove, while keeping track of pixels already removed
    pixels_to_remove = True
    while pixels_to_remove:

        # Randomly select pixels to remove
        pixels_x = np.random.uniform(0, width, int(data_cum[date]/scaling)).astype(int)
        pixels_y = np.random.uniform(0, height, int(data_cum[date]/scaling)).astype(int)

        # Check if these pixels have been removed before
        x_true = pd.Series(removed_pixels_x).isin(pixels_x) #TODO find beter var name
        y_true = pd.Series(removed_pixels_y).isin(pixels_y)

        if (x_true.any() and y_true.any):
            pass # Keep trying, very inefficient
        else:
            pixels_to_remove = False

    # Keep track of removed pixels
    removed_pixels_x = np.append(removed_pixels_x, pixels_x)
    removed_pixels_y = np.append(removed_pixels_y, pixels_y)

    # Make pixels white
    flag[removed_pixels_y, removed_pixels_x] = (255, 255, 255)
    frame = cv2.putText(flag, date, (0,100), font, 3, (0, 255, 0), 2, cv2.LINE_AA) # Add date to picture
    video.write(frame)

video.release()
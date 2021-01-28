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
dates_to_process = 25 # Number of data entries to process for testing, set to false for all

# Load data
data = pd.read_excel('data/COVID19BE.xlsx', sheet_name="CASES_AGESEX", index_col="DATE")
flag_orig = cv2.imread("data/Flag_of_Belgium.png") # flag_orig = cv2.cvtColor(flag_orig, cv2.COLOR_BGR2RGB) # For use in matplotlib
height, width = flag_orig.shape[:2]

# Format data
data = data.dropna() # Drop final nan entries
data = data.groupby(["DATE"]).sum() # Get total number of cases per day, groups municipality, age and sex together
data_cum = data["CASES"].cumsum() # Get cumulative number of cases per day
total_cases = data_cum[-1] # Total number of cases in Belgium so far

# Start video writer
fourcc = cv2.VideoWriter_fourcc(*'MP42')
video = cv2.VideoWriter('results/flag_cases.avi', fourcc, float(FPS), (width, height))

# Loop over all dates and create frame for every entry
scaling = flag_orig.size/total_cases # Remove pixels relative to population
removed_pixels_x = np.array([], dtype=int) # x-coordinates of pixels to be removed in the current frame
removed_pixels_y = np.array([], dtype=int) # y-coordinates of pixels to be removed in the current frame
for date in data_cum.keys()[0:dates_to_process]:
    print("Processing day: " + date)
    flag = copy.deepcopy(flag_orig)

    # Determine which pixels to remove, while keeping track of pixels already removed
    pixels_to_remove = int(data_cum[date]/scaling)
    pixels_x = np.array([], dtype=int)
    pixels_y = np.array([], dtype=int)
    while pixels_to_remove > 0:

        # Randomly select pixels to remove, based on how many are still left
        pixels_x_i = np.random.uniform(0, width, pixels_to_remove).astype(int)
        pixels_y_i = np.random.uniform(0, height, pixels_to_remove).astype(int)

        # Check if these pixels have been removed before
        x_true = pd.Series(removed_pixels_x).isin(pixels_x_i) #TODO find beter var name
        y_true = pd.Series(removed_pixels_y).isin(pixels_y_i)

        if (x_true.any() and y_true.any):
            n_duplicate = len(np.where(x_true)) # Number of duplicate entries, need to resample these
            index_x_duplicate = np.where(x_true)
            index_y_duplicate = np.where(y_true)

            # TODO find which pixels are okay, and which should still be removed
            pixels_to_remove = n_duplicate # Keep trying, very inefficient
            print("Duplicate pixles left: ", pixels_to_remove)
            pixels_x = np.append(pixels_x, pixels_x_i)
            pixels_y = np.append(pixels_y, pixels_y_i)

        else:
            pixels_x = np.append(pixels_x, pixels_x_i)
            pixels_y = np.append(pixels_y, pixels_y_i)
            pixels_to_remove = 0

    # Keep track of removed pixels
    removed_pixels_x = np.append(removed_pixels_x, pixels_x)
    removed_pixels_y = np.append(removed_pixels_y, pixels_y)

    # Make pixels white
    flag[removed_pixels_y, removed_pixels_x] = (255, 255, 255)
    frame = cv2.putText(flag, date, (0,100), font, 3, (0, 255, 0), 2, cv2.LINE_AA) # Add date to picture
    video.write(frame)

video.release()
print("Done")
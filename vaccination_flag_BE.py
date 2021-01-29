#!/usr/bin/env python2
# @brief visualization of current vaccination status in Belgium. Per vaccination, more pixels are drawn of the country flag.
# @detail Pixels are randomly sampled on every run.
# @author Robin Amsters
# @bug All injections are taken into account, so second doses are counted double

# Data source: https://covid-vaccinatie.be/nl (sciensano does not allow excell download as far as I could tell)
#  https://www.kaggle.com/gpreda/covid-world-vaccination-progress
# Flag image source: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg
# Inspiration: https://www.reddit.com/r/dataisbeautiful/comments/jotgob/one_pixel_per_us_covid19_death_oc/

# TODO animation
# new idea: put all coordinates in a list. Randomly select one with random.sample, and remove elements
# Idea: make it relative to the belgian map? Instead of flag? Could even use "gewest" data to make it more accurate

import cv2
import copy
import numpy as np
import pandas as pd
import random

# Parameters
inhabitants = 11492641  # https://statbel.fgov.be/nl/themas/bevolking/structuur-van-de-bevolking
add_date = False # add date to flag
font = cv2.FONT_HERSHEY_SIMPLEX

# Load data
data = pd.read_excel("data/vaccins-toegediend.xls")
flag = cv2.imread("data/Flag_of_Belgium.png")
height, width = flag.shape[:2]
n_pixels = height*width

# Format data
# If a date has the same 'gewest' twice, the second entry are second vaccinations. Don't want these in the flag for now
previous_date = ""
previous_gewest = ""
index_second_vaccination = np.array([])
for index, row in data.iterrows():
    current_date = row['Datum']
    current_gewest = row['Gewest']

    if (current_date == previous_date and current_gewest == previous_gewest):
        index_second_vaccination = np.append(index_second_vaccination, index)
    previous_date = current_date
    previous_gewest = current_gewest

# Split data in first and second round of vaccinations
data_second_vaccination = pd.DataFrame(columns=data.columns)
data_second_vaccination = data_second_vaccination.append(data.loc[index_second_vaccination, :])
data_first_vaccination = data.drop(index_second_vaccination)

data_first_vaccination = data_first_vaccination.groupby(["Datum"]).sum() # Get total number of cases per day, groups municipality, age and sex together
data_first_vaccination.index  = pd.to_datetime(data_first_vaccination.index, format="%d/%m/%Y")# After grouping date sorting is fucked, 2020 comes before 2021, fix it here
data_first_vaccination = data_first_vaccination.sort_index()
data_cum = data_first_vaccination["Dosissen toegediend"].cumsum() # Get cumulative number of cases per day
total_vaccinations = data_cum[-1] # Total number of cases in Belgium so far

# Prepare pixel grid
xvalues = np.arange(width)
yvalues = np.arange(height)
xx, yy = np.meshgrid(xvalues, yvalues)
pixels = np.dstack([xx, yy]).reshape(-1, 2)

# Randomly select pixels to draw based on number of vaccinations
# random.sample does not return duplicates: https://pynative.com/python-random-choice/
scaling = inhabitants/n_pixels # Draw pixels relative to population. Flag should be full when the entire population is vaccinated
pixels_to_draw = np.asarray(random.sample(pixels.tolist(), int(total_vaccinations/scaling))) # go to list and back to array as random.sample needs a list
pixels_x = pixels_to_draw[:,0]
pixels_y = pixels_to_draw[:,1]

# Draw flag
flag_vaccination = copy.deepcopy(flag)
flag_vaccination[:, :] = (255, 255, 255) # All white pixels of the right size
flag_vaccination[pixels_y, pixels_x] = flag[pixels_y, pixels_x] # opencv images have y,x index for some reason
final_date = data['Datum'][len(data['Datum'])-1]
flag_vaccination = cv2.putText(flag_vaccination, final_date, (0, 100), font, 3, (0, 255, 0), 2, cv2.LINE_AA)  # Add date to picture

flag_vaccination[1000, 100] = (255, 0, 0)
flag_vaccination = cv2.putText(flag_vaccination, "Pixel voor jolien", (100+10, 1000), font, 1, (255, 0, 0), 2, cv2.LINE_AA)  # Add date to picture

cv2.imshow("Vaccination flag", flag_vaccination)

# Save results
final_date_split = final_date.split("/")
final_date_underscore = final_date_split[0] + "_" + final_date_split[1] + "_" + final_date_split[2] # Seperate date month and year by underscores to propoerly save file
cv2.imwrite("results/flag_vaccination_" + final_date_underscore + ".png", flag_vaccination)

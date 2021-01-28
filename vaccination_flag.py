#!/usr/bin/env python2
# @brief visualization of current vaccination status in Belgium. Per vaccination, more pixels are drawn of the country flag.
# @detail Pixels are randomly sampled on every run.
# @author Robin Amsters
# @bug All injections are taken into account, so second doses are counted double

# Data source: https://covid-vaccinatie.be/nl (sciensano does not allow excell download as far as I could tell)
# Flag image source: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg
# Inspiration: https://www.reddit.com/r/dataisbeautiful/comments/jotgob/one_pixel_per_us_covid19_death_oc/

# TODO remove second injection duplicates
# TODO animation
# new idea: put all coordinates in a list. Randomly select one with random.sample, and remove elements
# Idea make it relative to the belgian map?

import cv2
import copy
import numpy as np
import pandas as pd
import random

# Parameters
inhabitants = 11492641  # https://statbel.fgov.be/nl/themas/bevolking/structuur-van-de-bevolking

# Load data
data = pd.read_excel('data/vaccins-toegediend.xls', index_col="Datum")
flag = cv2.imread("data/Flag_of_Belgium.png")
height, width = flag.shape[:2]
n_pixels = height*width

# Format data
data = data.groupby(["Datum"]).sum() # Get total number of cases per day, groups municipality, age and sex together
data_cum = data["Dosissen toegediend"].cumsum() # Get cumulative number of cases per day
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
cv2.imshow("Vaccination flag", flag_vaccination)
cv2.imwrite("results/flag_vaccination.png", flag_vaccination)
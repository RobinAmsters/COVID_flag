#!/usr/bin/env python2
# @brief 
# @author Robin Amsters
# @bug No known bugs

# Data source: https://covid-vaccinatie.be/nl
# Flag image source: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg
# Inspiration: https://www.reddit.com/r/dataisbeautiful/comments/jotgob/one_pixel_per_us_covid19_death_oc/

# Idea make it relative to the belgian map?
# TODO check that there are no duplicate pixels. The random sampling can take the same thing twice

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy

# Parameters
inhabitants = 11492641  # https://statbel.fgov.be/nl/themas/bevolking/structuur-van-de-bevolking

# Load data
data = pd.read_excel('data/vaccins-toegediend.xls', index_col="Datum")
flag = cv2.imread("data/Flag_of_Belgium.png")
height, width = flag.shape[:2]

# Format data
data = data.groupby(["Datum"]).sum() # Get total number of cases per day, groups municipality, age and sex together
data_cum = data["Dosissen toegediend"].cumsum() # Get cumulative number of cases per day
total_vaccinations = data_cum[-1] # Total number of cases in Belgium so far

scaling = flag.size/total_vaccinations # Draw pixels relative to population

pixels_x = np.random.uniform(0, width, int(total_vaccinations / scaling)).astype(int)
pixels_y = np.random.uniform(0, height, int(total_vaccinations / scaling)).astype(int)

# Make pixels white
flag_vaccination = copy.deepcopy(flag)
flag_vaccination[:, :] = (255, 255, 255) # All white pixels of the right size
flag_vaccination[pixels_y, pixels_x] = flag[pixels_y, pixels_x]
cv2.imshow("Vaccination flag", flag_vaccination)
# @brief visualization of current vaccination status in Belgium, represented as a country flag
# @detail More pixels are drawn as more people get their (first) vaccination. This is relative to the total population.
# I.e., 1 pixel does not equal 1 vaccination. When the entire population is vaccinated, the flag will be full.
# Pixels are randomly sampled on every run, so subsequent runs will look different
# @author Robin Amsters
# @bug Flags are not all of the same size
# @bug Some flags need a bright background (if they have black in them) and others need a dark background
# (if there is white in the flag). This does not make for the best comparison.

# Data: https://www.kaggle.com/gpreda/covid-world-vaccination-progress

# Flag image sources:
#  - Belgium: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg
#  - Netherlands: https://nl.wikipedia.org/wiki/Vlag_van_Nederland#/media/Bestand:Flag_of_the_Netherlands.svg
#  - Germany: https://en.wikipedia.org/wiki/Flag_of_Germany#/media/File:Flag_of_Germany.svg
# - United States: https://en.wikipedia.org/wiki/United_States#/media/File:Flag_of_the_United_States.svg
# - UK: https://en.wikipedia.org/wiki/United_Kingdom#/media/File:Flag_of_the_United_Kingdom.svg

# Inhabitants sources:
# - https://en.wikipedia.org/wiki/Belgium
# - https://en.wikipedia.org/wiki/Netherlands
# - https://en.wikipedia.org/wiki/Germany
# - https://en.wikipedia.org/wiki/United_States
# - https://en.wikipedia.org/wiki/China
# - https://en.wikipedia.org/wiki/France
# - https://en.wikipedia.org/wiki/France

# Inspiration: https://www.reddit.com/r/dataisbeautiful/comments/jotgob/one_pixel_per_us_covid19_death_oc/

# TODO format flags so they are all the same size. Maybe make some space around it?

import cv2
import copy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

# Parameters
add_date = False # add date to flag
font = cv2.FONT_HERSHEY_SIMPLEX
n_rows = 2 # Number of subplot rows
n_cols = 3 # Number of subplot columns

# Country data
# countries_to_plot = ["Belgium", "Netherlands", "Germany", "United States", "Israel", "United Kingdom", "China", "France"]
#background = [(255,255,255), (0, 0, 0), (255,255,255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255,255,255), (0, 0, 0)] # What should the non-filled in pictures have as color, should be in same order as countries
# inhabitants = [11492641, 17469635, 83166711, 328239523, 9305020, 67886004, 1400050000, 67407000] # Total inhabitants per country, should be in same order as countries

countries_to_plot = [ "United States", "Israel", "United Kingdom", "China", "India", "Russia"]
inhabitants = [328239523, 9305020, 67886004, 1400050000, 1352642280, 146238185] # Total inhabitants per country, should be in same order as countries


# Load data
data = pd.read_csv("data/vaccination/country_vaccinations.csv")

for i in range(len(countries_to_plot)):
    country = countries_to_plot[i]

    flag = cv2.imread("data/flags/Flag_of_" + country +".png")
    flag = cv2.cvtColor(flag, cv2.COLOR_BGR2RGB)
    height, width = flag.shape[:2]
    n_pixels = height*width

    # Get total number of vaccinations
    data_country = data.loc[data["country"] == country]
    vaccination_index = data_country.index[-1]
    total_vaccinations = data_country["total_vaccinations"][vaccination_index]

    # Prepare pixel grid
    xvalues = np.arange(width)
    yvalues = np.arange(height)
    xx, yy = np.meshgrid(xvalues, yvalues)
    pixels = np.dstack([xx, yy]).reshape(-1, 2)

    # Randomly select pixels to draw based on number of vaccinations
    # random.sample does not return duplicates: https://pynative.com/python-random-choice/
    scaling = inhabitants[i]/n_pixels # Draw pixels relative to population. Flag should be full when the entire population is vaccinated
    pixels_to_draw = np.asarray(random.sample(pixels.tolist(), int(total_vaccinations/scaling))) # go to list and back to array as random.sample needs a list
    pixels_x = pixels_to_draw[:,0]
    pixels_y = pixels_to_draw[:,1]

    # Draw flag
    flag_vaccination = copy.deepcopy(flag)
    flag_vaccination[:, :] = (166, 166, 166)
    flag_vaccination[pixels_y, pixels_x] = flag[pixels_y, pixels_x] # opencv images have y,x index for some reason
    final_date = data_country["date"][vaccination_index]

    subplot_index = n_rows*100 + n_cols*10 + 1 + i
    plt.subplot(subplot_index)
    plt.title(country + " " + final_date)
    plt.imshow(flag_vaccination)

plt.tight_layout()

    #cv2.imshow("Vaccination flag", flag_vaccination)

    # Save results
    #cv2.imwrite("results/flag_vaccination_"+ country + "_" + final_date + ".png", flag_vaccination)

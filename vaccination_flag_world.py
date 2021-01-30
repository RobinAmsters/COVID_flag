# @brief visualization of current vaccination status in Belgium, represented as a country flag
# @detail More pixels are drawn as more people get their (first) vaccination. This is relative to the total population.
# I.e., 1 pixel does not equal 1 vaccination. When the entire population is vaccinated, the flag will be full.
# Pixels are randomly sampled on every run, so subsequent runs will look different
# @author Robin Amsters
# @bug No known bugs

# Data: https://www.kaggle.com/gpreda/covid-world-vaccination-progress

# Flag image sources:
#  - Belgium: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg
#  - Netherlands: https://nl.wikipedia.org/wiki/Vlag_van_Nederland#/media/Bestand:Flag_of_the_Netherlands.svg
#  - Germany: https://en.wikipedia.org/wiki/Flag_of_Germany#/media/File:Flag_of_Germany.svg
# - United States: https://en.wikipedia.org/wiki/United_States#/media/File:Flag_of_the_United_States.svg

# Inhabitants sources:
# - https://en.wikipedia.org/wiki/Belgium
# - https://en.wikipedia.org/wiki/Netherlands
# - https://en.wikipedia.org/wiki/Germany
# - https://en.wikipedia.org/wiki/United_States

# Inspiration: https://www.reddit.com/r/dataisbeautiful/comments/jotgob/one_pixel_per_us_covid19_death_oc/


import cv2
import copy
import numpy as np
import pandas as pd
import random

# Parameters
add_date = False # add date to flag
font = cv2.FONT_HERSHEY_SIMPLEX
countries_to_plot = ["Belgium", "Netherlands", "Germany", "United States"]
# TODO isreal, UK,
background = [(255,255,255), (0, 0, 0), (255,255,255), (0, 0, 0)] # What should the non-filled in pictures have as color, should be in same order as countries
inhabitants = [11492641, 17469635, 83166711, 328239523] # Total inhabitants per country, should be in same order as countries

# Load data
data = pd.read_csv("data/vaccination/country_vaccinations.csv")

for i in range(len(countries_to_plot)):
    country = countries_to_plot[i]

    flag = cv2.imread("data/flags/Flag_of_" + country +".png")
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
    flag_vaccination[:, :] = background[i]
    flag_vaccination[pixels_y, pixels_x] = flag[pixels_y, pixels_x] # opencv images have y,x index for some reason
    final_date = data_country["date"][vaccination_index]
    flag_vaccination = cv2.putText(flag_vaccination, final_date, (0, 100), font, 3, (0, 255, 0), 2, cv2.LINE_AA)  # Add date to picture

    #cv2.imshow("Vaccination flag", flag_vaccination)

    # Save results
    cv2.imwrite("results/flag_vaccination_"+ country + "_" + final_date + ".png", flag_vaccination)

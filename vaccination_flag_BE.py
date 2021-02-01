# @brief visualization of current vaccination status in Belgium, represented as a country flag
# @detail More pixels are drawn as more people get their (first) vaccination. This is relative to the total population.
# I.e., 1 pixel does not equal 1 vaccination. When the entire population is vaccinated, the flag will be full.
# Pixels are randomly sampled on every run, so subsequent runs will look different
# @author Robin Amsters
# @bug No known bugs

# Inspiration: https://www.reddit.com/r/dataisbeautiful/comments/jotgob/one_pixel_per_us_covid19_death_oc/
# Data source: https://covid-vaccinatie.be/nl (sciensano does not allow excell download as far as I could tell)
# Flag image source: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg

# TODO update for new data format, which more nicely splits first and second round of vaccination

import cv2
import copy
import numpy as np
import pandas as pd
import random

# Parameters
inhabitants = 11492641  # Estimate at Januari 2020: https://statbel.fgov.be/nl/themas/bevolking/structuur-van-de-bevolking
add_date = True # Add date to flag
font = cv2.FONT_HERSHEY_SIMPLEX # Font for date
animation = True # if set to false, only the most recent flag will be drawn
FPS = 3 # for animation if set to true

# Load data
data = pd.read_excel("data/vaccination/vaccins-toegediend.xls")
flag = cv2.imread("data/flags/Flag_of_Belgium.png")
height, width = flag.shape[:2]
n_pixels = height*width
scaling = inhabitants / n_pixels  # Draw pixels relative to population. Flag should be full when the entire population is vaccinated
final_date = data['Datum'][len(data['Datum']) - 1]
final_date_split = final_date.split("/")
final_date_underscore = final_date_split[0] + "_" + final_date_split[1] + "_" + final_date_split[
    2]  # Seperate date month and year by underscores to propoerly save file

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

# Get total number of vaccinations
# Note: simply copying the total number of vaccinations would be a lot quicker, but part of the goal of this project is
# for me to get more familiar with pandas.
data_first_vaccination = data_first_vaccination.groupby(["Datum"]).sum() # Get total number of cases per day, groups municipality, age and sex together
data_first_vaccination.index  = pd.to_datetime(data_first_vaccination.index, format="%d/%m/%Y") # After grouping date sorting is messed up, 2020 comes before 2021, fix it here
data_first_vaccination = data_first_vaccination.sort_index()
data_cum = data_first_vaccination["Dosissen toegediend"].cumsum() # Get cumulative number of cases per day

# Prepare pixel grid
xvalues = np.arange(width)
yvalues = np.arange(height)
xx, yy = np.meshgrid(xvalues, yvalues)
pixels = np.dstack([xx, yy]).reshape(-1, 2)

if animation:
    # Start video writer
    fourcc = cv2.VideoWriter_fourcc(*'MP42')
    video = cv2.VideoWriter("results/flag_vaccination_" + final_date_underscore + ".avi", fourcc, float(FPS), (width, height))

    # flatten image indexes for easier sampling of frames (removal of sampled pixels)
    xx = xx.flatten()
    yy = yy.flatten()
    pixels_index = range(len(xx)) # an index for every pixel

    # Keep track of pixels that have already been drawn
    pixels_x = np.array([], dtype=int)
    pixels_y = np.array([], dtype=int)

    for index, row in data_first_vaccination.iterrows(): # make a flag for every dag in the data
        date_i = index.strftime("%d-%m-%Y")
        vaccinations_i = row['Dosissen toegediend']

        # Prepare flag
        flag_vaccination = copy.deepcopy(flag)  # Make a copy of the original flag to get the size right
        flag_vaccination[:, :] = (255, 255, 255)  # Make all pixels white

        # when making a frame:
        # 1. Randomly select indexes from the pixels that are still white (not sampled)
        # 2. Fill in the pixels that have this index with their original values
        # 3. Draw flag
        # 4. Remove the colored pixels from consideration for the next round of sampling

        # Randomly select pixels to draw based on number of vaccinations
        # random.sample does not return duplicates: https://docs.python.org/3/library/random.html
        pixels_to_draw_index = np.asarray(random.sample(pixels_index, int(vaccinations_i / scaling)))  # go to list and back to array

                                                                                        # as random.sample needs a list
        if len(pixels_to_draw_index) > 0:
            pixels_x = np.append(pixels_x, xx[pixels_to_draw_index])
            pixels_y = np.append(pixels_y, yy[pixels_to_draw_index])

        # Draw flag
        flag_vaccination[pixels_y.tolist(), pixels_x.tolist()] = flag[pixels_y, pixels_x]  # Draw original color for selected pixels. opencv images have y,x index for some reason

        if add_date:
            flag_vaccination = cv2.putText(flag_vaccination, date_i, (0, 100), font, 3, (0, 255, 0), 2,
                                           cv2.LINE_AA)  # Add date to picture as text

        video.write(flag_vaccination)

    video.release()

else:
    total_vaccinations = data_cum[-1] # Total number of cases in Belgium so far

    # Prepare flag
    flag_vaccination = copy.deepcopy(flag)  # Make a copy of the original flag to get the size right
    flag_vaccination[:, :] = (255, 255, 255)  # Make all pixels white

    # Randomly select pixels to draw based on number of vaccinations
    # random.sample does not return duplicates: https://docs.python.org/3/library/random.html
    pixels_to_draw = np.asarray(random.sample(pixels.tolist(), int(total_vaccinations/scaling))) # go to list and back to array as random.sample needs a list
    pixels_x = pixels_to_draw[:,0]
    pixels_y = pixels_to_draw[:,1]

    # Draw flag
    flag_vaccination[pixels_y, pixels_x] = flag[pixels_y, pixels_x] # Draw original color for selected pixels. opencv images have y,x index for some reason
    if add_date:
        flag_vaccination = cv2.putText(flag_vaccination, final_date, (0, 100), font, 3, (0, 255, 0), 2, cv2.LINE_AA)  # Add date to picture as text

    # Save results
    cv2.imwrite("results/flag_vaccination_" + final_date_underscore + ".png", flag_vaccination)

# Vaccination flag

Current degree of vaccination in Belgium, represented as the country flag. More pixels are drawn as more people get their (first) vaccination. This is relative to the total population,  so 1 pixel does not equal 1 vaccination. When the entire population is vaccinated, the flag will be full. 

Pixels are randomly sampled on every run, so subsequent runs will look different.



## Dependencies

- copy
- numpy
- pandas
- random



## To generate a of Belgium flag yourself

1. download this repository
2. download data [vaccination data](https://covid-vaccinatie.be/nl ) (flags are included because public domain) and store in data/vaccinations folder. 
3. run vaccination_flag_BE.py
   1. optionally set 'animation' to true to make a video of all the data

## To compare flags of multiple countries
1. Download this repository
2. Download [world vaccincation data](ttps://www.kaggle.com/gpreda/covid-world-vaccination-progress) (make sure the countries you want to plot are in the dataset)
3. Set the countries you want to compare in "countries_to_plot"
   - Make sure set the "inhabitants" as well
   - For every country in "countries_to_plot", there should be a flag the data.flags/ folder. The expected name of the flag is Flag_of_COUNTRY.png
   - The number of suplots can be adjusted in n_rows and n_cols



# References 

Inspiration for this project: https://www.reddit.com/r/dataisbeautiful/comments/jotgob/one_pixel_per_us_covid19_death_oc/# 

Data source: https://covid-vaccinatie.be/nl 

Flag image source: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg




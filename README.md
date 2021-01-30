# Vaccination flag

Current degree of vaccination in Belgium, represented as the country flag. More pixels are drawn as more people get their (first) vaccination. This is relative to the total population,  so 1 pixel does not equal 1 vaccination. When the entire population is vaccinated, the flag will be full. 

Pixels are randomly sampled on every run, so subsequent runs will look different.



## Dependencies

- copy
- numpy
- pandas
- random



## To generate a flag yourself

1. download this repository

2. download data [vaccination data](https://covid-vaccinatie.be/nl ) (flags are included because public domain) and store in data/vaccinations folder. 
3. run vaccination_flag_BE.py



# References 

Inspiration for this project: https://www.reddit.com/r/dataisbeautiful/comments/jotgob/one_pixel_per_us_covid19_death_oc/# 

Data source: https://covid-vaccinatie.be/nl 

Flag image source: https://en.wikipedia.org/wiki/Flag_of_Belgium#/media/File:Flag_of_Belgium.svg




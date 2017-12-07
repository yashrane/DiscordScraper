#DiscordScraper
This is a data collection and analysis script written for UCSB's discord server. Data collection was done using the discord.py module. The analysis can be split into two parts: a toxicity predictor and demographic/message data visualizations.

## Toxicity Predictions
Written by Brian Lim with help from Kitty Fung

WIP

## Data Visualizations
Written in R by Yash Rane

### Introduction Data
Our scraper script outputs all introductions to a file named introductions.csv, with all names removed in order to preseve anonymity.Introductions came in all kinds of formats, so it was impossible to create a single regex pattern that could parse an introduction. Because of this, the code for loading in introduction data had to deal with a large number of edge cases, and no clean solution could be found. These cleaned introductions were loaded into a dataframe, and could then be accessed by the parts of the project that create plots.





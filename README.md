# DiscordScraper
This is a data collection and analysis script written for UCSB's discord server. Data collection was done using the discord.py module. The analysis can be split into two parts: a toxicity predictor and demographic/message data visualizations.

## Toxicity Predictions
Written by Brian Lim with help from Kitty Fung

WIP

## Data Visualizations
Written in R by Yash Rane

#### Introduction Data
Our scraper script outputs all introductions to a file named introductions.csv, with all names removed in order to preserve anonymity.Introductions came in all kinds of formats, so it was impossible to create a single regex pattern that could parse an introduction. Because of this, the code for loading in introduction data had to deal with a large number of edge cases, and no clean solution could be found. These cleaned introductions were loaded into a dataframe, and could then be accessed by the parts of the project that create plots.

<p align="center">
<img src="https://raw.githubusercontent.com/yashrane/DiscordScraper/master/plots/img/major_plot.png">
</p>

The majority of students here are studying some kind of science, but since there are more kinds of science majors, this is no surprise. Math (which includes things like Econ and Stats) and Humanities, on the other hand, are much higher than I initally expected. This is especially surprising for Math, since it encompasses the smallest number of majors.

<p align="center">
<img src="https://raw.githubusercontent.com/yashrane/DiscordScraper/master/plots/img/year_and_found_from_plot.png">
</p>

Looking at the distribution of class years, it's pretty clear that the chat is dominated by freshman, with almost twice as many freshman as any other group. The vast majority of people found the discord through reddit, no doubt because it is permanantly pinned on the UCSB subreddit's front page. From this, I can resonably assume that our demographics resemble reddit's (2/3 Male). 
Freshman also have the highest proportion of people who found the chat server either through a friend or through facebook.


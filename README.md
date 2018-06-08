# DiscordScraper
By Yash Rane and Brian Lim, with help from Kitty Fung

UCSB's Discord chat server has been growing quickly over the past year, and this rapid growth has made moderation harder and harder. We wanted to find a way to make managing the server easier, so we built a set of moderator tools.
First, we created a Discord bot using the discord.py module to compile a record of all chat logs. Then, we designed a recurrent neural network to analyze the toxicity of these messages. Finally, we took the data collected from the bot, and the toxicity predictions from the RNN, and created a dashboard that moderators could use to manage and monitor the server.

## Data Collection
The discord.py module allows us to easily create a bot that scrapes each message that gets sent in the server and logs that message to a .csv file. This gives us a convinent way of organizing the data for later analysis. A sample data observation is shown below (toxicity score appended to data later)
<p align="center">
<img src="https://raw.githubusercontent.com/yashrane/DiscordScraper/master/img/data_obs.PNG">
</p>


## Toxicity Analysis
We created an LSTM with both word embeddings (using word2vec) and character-wise embeddings. Our network architecture is shown below.
<p align="center">
<img src="https://raw.githubusercontent.com/yashrane/DiscordScraper/master/img/architecture.PNG">
</p>

Our model was trained on the Google Jigsaw Toxicity data, taken from kaggle.com. We acheived an ROC AUC of 0.88. Google's state-of-the-art model recieved a score of 0.99, but considering that we don't have access to the same kind of resouces that Google does, our score is still impressive.
<p align="center">
<img src="https://raw.githubusercontent.com/yashrane/DiscordScraper/master/img/ROC.PNG">
</p>


## Dashboard
<p align="center">
<img src="https://raw.githubusercontent.com/yashrane/DiscordScraper/master/img/dashboard.PNG">
</p>

Our dashboard was created using plot.ly's dash library for python. On the left side, there are the introductions - information that a moderator could immediately act on. This is especially important to us that we display actionable data, since theres no point showing information that you can't do anything about. On the right side, we have the monitoring portion. This includes a graph of how active the server has been over the past day, and the average toxicity over the same time span.

## Misc Data Visualizations
<p align="center">
<img src="https://raw.githubusercontent.com/yashrane/DiscordScraper/master/img/Years.png">
</p>

Looking at the distribution of class years, it's pretty clear that the chat is dominated by freshman, with almost twice as many freshman as any other group. This is reflected in some of our freshman-oriented channels, such as `#questions` and `#roommates-finder`, which are both dominated by incoming first years

setwd('C:/Users/yashr/Documents/Random Projects/DiscordScraper/plots')
library('ggplot2')
library('lubridate')

messages = read.csv('../messages.csv')



#format string to parse the timestamps with
#Only keeping precision to the minute
time_format <- "%F %H:%M"

#converts the timestamp column to time objects
messages$Timestamp <- strptime(x=messages$Timestamp, format = time_format)

ggplot(messages, aes(x=lapply(messages$Timestamp,FUN=round_date, unit='hour'))) + geom_line(stat='count')

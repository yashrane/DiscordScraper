setwd('C:/Users/yashr/Documents/Random Projects/DiscordScraper/plots')
library('ggplot2')
library('lubridate')
library('dplyr')


messages = read.csv('../messages.csv', stringsAsFactors = FALSE)



#format string to parse the timestamps with
#Only keeping precision to the minute
time_format <- "%F %H:%M"

#converts the timestamp column to time objects
messages$Timestamp <- strptime(x=messages$Timestamp, format = time_format)

makeRoleColumns <- function(){
  
  
  pattern <- "'(.+?)'"
  roles <- str_match_all(messages$Roles[1], pattern)[[1]][,2]
  
  appendNewRoles <- function(role_str){
    parsed_roles <- str_match_all(role_str, pattern)[[1]][,2]
    new_roles <- setdiff(parsed_roles, colnames(messages))
    messages = cbind(colnames(messages), new_roles)
    #roles = list(roles, list(new_roles))
  }
}





# TODO: make a plot showing how active the chat is over time
#to start with, just make a generic plot of acivity over the entire dataset
#later, we may want to have different kinds of views to show the data in different time range (1 week at a time, 1 month, 1 day, etc)



# Note: #' @ param is how you do docs in R
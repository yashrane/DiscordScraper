setwd('C:/Users/yashr/Documents/Random Projects/DiscordScraper/plots')
library('ggplot2')
library('lubridate')
library('dplyr')
library('stringr')


messages = read.csv('../messages.csv', stringsAsFactors = FALSE)



#format string to parse the timestamps with
#Only keeping precision to the minute
time_format <- "%F %H:%M"

date1 <- as.Date("2017-10-12")
date2 <- as.Date("2017-10-14")

#converts the timestamp column to time objects
messages$Timestamp <- strptime(x=messages$Timestamp, format = time_format)

#test <- messages[messages$Timestamp > date1 & messages$Timestamp < date2,]
#messages$Month <- month(messages$Timestamp)
#messages$Day <- day(messages$Timestamp)
#messages$Hour <- hour(messages$Timestamp)
#messages$Minute <- minute(messages$Timestamp)



#' returns a list of unique string from a column of list strings
#' @param role_col the column that contains list of roles
#' @noRd
get_unique_roles <- function(role_col){
  
  #' helper function for get_unique_roles that parses a list string into a list of its contents
  #' @param list_str the column that contains list of roles
  #' @noRd
  parse_role_string <- function(list_str){
    pattern <- "'([^']+)'" #regex that selects the contents of a stringified list
    roles <- str_match_all(list_str, pattern)[[1]][,2]
    return(roles)
  }
  
  
  roles <- lapply(role_col, parse_role_string)
  unique_roles <- Reduce(union,roles) #performs a set union on each list
  
  return(unique_roles)
}


#' Creates a dataframe from a columns of roles. Each column represents whether that role exists for the row or not
#' @param role_col the columns that contains the list of roles. each list must be a string
#' @param keep_roles optional parameter that specifies which roles to use. If unspecified, all roles will be used
#' @noRd
make_role_df <- function(role_col, keep_roles){
  
  if(missing(keep_roles)){
    keep_roles <- get_unique_roles(role_col)
  }
  
  role_data <-lapply(role_col,function(list_str) str_detect(list_str, keep_roles))
  role_df <- as.data.frame(do.call(rbind, role_data))#converts the list role_data into a dataframe
  colnames(role_df) <- keep_roles
  
  return(role_df)
}

role_df <- make_role_df(messages$Roles, c('Members','Gauchito', 'Regular'))

#message_plot <- ggplot(data=messages, aes(x=Timestamp)) + 
#  geom_line(stat='count')  
#message_plot





# TODO: make a plot showing how active the chat is over time
#to start with, just make a generic plot of acivity over the entire dataset
#later, we may want to have different kinds of views to show the data in different time range (1 week at a time, 1 month, 1 day, etc)



# Note: #' @ param is how you do docs in R
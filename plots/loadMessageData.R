#setwd('C:/Users/yashr/Documents/Random Projects/DiscordScraper/plots')
library('ggplot2')
library('lubridate')
library('dplyr')
library('stringr')



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

load_message_data <- function(){
  messages = read.csv('./lib/messages.csv', stringsAsFactors = FALSE)
  
  #format string to parse the timestamps with
  #Only keeping precision to the minute
  time_format <- "%F %T"
  
  #converts the timestamp column to time objects
  messages$Timestamp <- with_tz(strptime(x=messages$Timestamp, format = time_format, tz="UTC"), "America/Los_Angeles")
#  messages$Timestamp <- strptime(x=messages$Timestamp, format = time_format)
  
  role_df <- make_role_df(messages$Roles, c('Members','Gauchito', 'Regular'))
  messages <- merge(messages, role_df,by="row.names")
  
  return(messages)
}



#we want 3 or 4 views: overarching, weekly/monthly, daily
make_message_graphs <- function(view){
  if(!exists("messages")){
    messages <- load_message_data()
  }
  
  if(identical(view, "Overview")){
    message_plot <- ggplot(data=messages, aes(x=round_date(Timestamp, unit = "day"))) + 
      geom_line(data=messages[messages$Gauchito, ], stat='count', aes(colour = "Freshman"))  +
      geom_line(stat='count', aes(colour = "Everyone")) +
      scale_color_manual(breaks = c("Everyone", "Freshman"), values = c("black", "red"))+
      labs(title = "Messages Over Time in the UCSB Discord", x ="Time", y="# of Messages") + 
      theme_gray(base_size = 25)+theme(legend.title = element_blank())
  }
  
  if(identical(view, "Day")){
   # message_plot <- ggplot(data=messages, aes(x=hour(Timestamp))) + 
   #   geom_bar(aes(y=..count..)) +
   #   labs(title = "Messages Throughout a Day in UCSB Friendos", x ="Hour", y="# of Messages") + 
   #   theme_gray(base_size = 20)
    
    message_plot <- ggplot(data=messages, aes(x=hour(Timestamp), colour="red")) + 
     geom_line(stat='count') +
     labs(title = "Messages Throughout a Day in the UCSB Discord", x ="Hour", y="# of Messages") + 
     theme_gray(base_size = 25) + theme(legend.position = "none")
  }
  
  if(identical(view, "Week")){
    message_plot <- ggplot(data=messages, aes(x=ordered(wday(Timestamp)), fill=ordered(wday(Timestamp)))) + 
      geom_bar(aes(y=..count..)) +
      scale_x_discrete(breaks = c(1,2,3,4,5,6,7), labels=c("Sun","Mon","Tues","Wed","Thurs", "Fri", "Sat")) +
      scale_fill_manual(values=c("gold", "royalblue1","gold", "royalblue1","gold", "royalblue1","gold"))+
      labs(title = "Messages Throughout a Day in the UCSB Discord", x ="Day", y="# of Messages") + 
      theme_gray(base_size = 25) + theme(legend.position = "none")
  }
  
  return(message_plot)
}

messages <- load_message_data()


message_plot <- ggplot(data=messages,aes(x=reorder(Channel, ..count..), y=..count..))+ 
  geom_bar()+ 
  coord_flip()
message_plot



# TODO: make a plot showing how active the chat is over time
#to start with, just make a generic plot of acivity over the entire dataset
#later, we may want to have different kinds of views to show the data in different time range (1 week at a time, 1 month, 1 day, etc)



# Note: #' @ param is how you do docs in R
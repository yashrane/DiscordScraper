setwd('C:/Users/yashr/Documents/Random Projects/DiscordScraper/plots')
library('ggplot2')
library('lubridate')
library('dplyr')
library('stringr')
library(googlesheets)
library('forcats')


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
#  return(role_data)
}


load_from_gsheet <- function(token, key){
#  gs_auth(token = token)
#  gap <- gs_key(key)
#  data <- gs_read(gap)
  
  uri = gs_webapp_auth_url(client_id = '877318179750-d7g9u88smnmcsrvcohngcp8n6l606j8r.apps.googleusercontent.com', 
                     redirect_uri = 'http://www.google.com/robots.txt')
  gs_webapp_get_token(uri)
    
  return(data)
}

createToken <- function(){
  token <- gs_auth(cache=FALSE)
  gd_token()
  saveRDS(token, file = "googlesheets_token.rds")
}

load_message_data <- function(){
  messages = read.csv('./lib/messages.csv', stringsAsFactors = FALSE, 
                      col.names = c("Roles", "Timestamp", "Channel", "Content", "User.ID", "Toxicity"))
 # messages = load_from_gsheet('googlesheets_token.rds',"1-C4S0ergLT5BEjC1RhhtRtCx1S_yxdx9a2WgjfSOOjM" )[1:4]
  
  
  
  #format string to parse the timestamps with
  #Only keeping precision to the minute
  time_format <- "%F %T"
  
  #converts the timestamp column to time objects
  messages$Timestamp <- with_tz(as.POSIXct(strptime(x=messages$Timestamp, format = time_format, tz="UTC")), "America/Los_Angeles")
#  messages$Timestamp <- strptime(x=messages$Timestamp, format = time_format)
  
  messages$User.ID = as.factor(messages$User.ID)
  
  role_df <- make_role_df(messages$Roles, c('Members','Gauchito', 'Regular'))#Look into using extract from tidyr for this
  messages <- merge(messages, role_df,by="row.names", all.x = TRUE)
  
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


plot_activity <- function(){
  last_message <- messages[nrow(messages),]$Timestamp
  past_day <- interval(last_message-ddays(), last_message)

  activity <- messages %>% filter(Timestamp %within% past_day)
  
  message_plot <- ggplot(data=activity, aes(x=Timestamp, colour="red")) + 
    geom_line(stat='count') +
    labs(title = "Messages Throughout a Day in the UCSB Discord", x ="Hour", y="# of Messages") + 
    theme_gray(base_size = 25) + theme(legend.position = "none")
}

usage_info<-function(){
  reg_table <- messages %>% group_by(User.ID) %>% na.omit() %>%
    summarize(count=n()/n_distinct(month(Timestamp)), IsReg = any(Regular), isMapachito = any(grepl("Mapachito", Roles))) 
  
  AddThreshold <- unlist(reg_table %>% filter(IsReg) %>% summarize(count=sum(count)/n()))
  reg_table$NeedReg <- reg_table$count > AddThreshold
  add_list <- reg_table %>% filter(!IsReg & NeedReg)
  
  RemoveThreshold <- unlist(reg_table  %>% summarize(count=sum(count)/n()))
  kill_list <- reg_table %>% filter(IsReg & count < RemoveThreshold)
  
  info <- list("add"=add_list$User.ID, "remove"=kill_list$User.ID)
  return(info)
}


interesting_user <- "285607618913894400"
messages <- load_message_data()

num_regulars <- messages %>% filter(Regular) %>% summarise(n_distinct(User.ID))
average_regular <-  sum((!is.na(messages$User.ID)) & messages$Regular & !grepl(interesting_user, messages$User.ID)) / num_regulars/ n_distinct(month(messages$Timestamp))

num_normals <- messages %>% filter(!Regular) %>% summarise(n_distinct(User.ID))
average_normal <-  sum((!is.na(messages$User.ID)) & !messages$Regular)/num_normals/ n_distinct(month(messages$Timestamp))

testplot <- ggplot(data=messages[!is.na(messages$User.ID) & !grepl(interesting_user, messages$User.ID),], 
  aes(x=fct_lump(fct_infreq(User.ID), n=20), fill=Regular)) + 
  stat_count() + geom_hline(yintercept = 1239) +
   coord_flip()

reg_table <- messages %>% group_by(User.ID) %>% na.omit() %>%
  summarize(count=n()/n_distinct(month(Timestamp)), IsReg = any(Regular), isMapachito = any(grepl("Mapachito", Roles))) 

#add if you talk more than the average regular
AddThreshold <- unlist(reg_table %>% filter(IsReg) %>% summarize(count=sum(count)/n()))
reg_table$NeedReg <- reg_table$count > AddThreshold
add_list <- reg_table %>% filter(!IsReg & NeedReg)

#Remove from regular if you talk less than the average person
RemoveThreshold <- unlist(reg_table  %>% summarize(count=sum(count)/n()))
kill_list <- reg_table %>% filter(IsReg & count < RemoveThreshold)


testplot <- ggplot(reg_table %>% filter(User.ID != interesting_user)) +
  geom_point(aes(x=User.ID, y=count, color=IsReg))+
  geom_hline(yintercept = AddThreshold)+geom_hline(yintercept = RemoveThreshold)
  

#messages %>% group_by(User.ID, month(Timestamp)) %>% summarize(n())

#-----------------------------------------------------
#look at unique user ids before a date

intros <-messages %>% 
#  filter(Channel == 'introductions') %>% 
  group_by(month(Timestamp), day(Timestamp)) %>% 
  summarize(count=n(), Timestamp=max(Timestamp))
ggplot(intros, aes(x=Timestamp, y=count))+geom_line()

toxic <-messages %>% 
  #  filter(Channel == 'introductions') %>% 
  group_by(month(Timestamp), day(Timestamp)) %>% 
  summarize(toxicity=mean(Toxicity, na.rm=T), Timestamp=max(Timestamp), n_users=n_distinct(User.ID))
ggplot(toxic[!is.na(toxic$toxicity),], aes(x=Timestamp, y=toxicity))+geom_line()


ggplot(messages, aes(Toxicity))+geom_histogram() #+ facet_wrap(~Channel)

head(messages %>% filter(Toxicity > 0.75) %>% arrange(desc(Toxicity)))
#-----------------------------------------------------

#How to tell if someone is a regular or not?
#find total messages by that user for the past month
#compare that number against the average regular for the past month/average month
#if higher, then they are regular

#find the different between active regulars and inactive regulars

#Create Some Kind of simple verification of admin, and only display the list of peeps to add and remvoe to 
#those admins






#message_plot <- ggplot(data=messages,aes(x=reorder(Channel, ..count..), y=..count..))+ 
#  geom_bar()+ 
#  coord_flip()
#message_plot



# TODO: make a plot showing how active the chat is over time
#to start with, just make a generic plot of acivity over the entire dataset
#later, we may want to have different kinds of views to show the data in different time range (1 week at a time, 1 month, 1 day, etc)



# Note: #' @ param is how you do docs in R
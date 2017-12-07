#setwd('C:/Users/yashr/Documents/Random Projects/DiscordScraper/plots')
library("stringr")





#' cleans Strings from the Year and School Columns
#' should be used with lapply
#' @param string the string to be cleaned
#' @return the cleaned string
#' @noRd
cleanYearAndSchool <- function(string){
  
  #year and school had similar problems with them, so it is easier to put them both into the same function
  temp <- tolower(string)
  temp <- str_replace_all(temp, "[\\s()]", "")#removes whitespace and parenthesis
  
  #Edge Cases
  temp <- str_replace_all(temp, "(ls|l&s)", "ucsb")
  temp <- str_replace_all(temp, "2017", "4")
  temp <- str_replace_all(temp, "sixmonths", "4")
  
  
  return(temp)
}



#' cleans Strings from the Major Column
#' should be used with lapply
#' @param string the string to be cleaned
#' @return the cleaned string
#' @noRd
cleanMajor <- function(string){
  temp <- tolower(string)
  temp <- str_trim(temp)
  temp <- str_replace_all(temp, "major", "")
  
    
  #lots of edge cases
  temp <- str_replace_all(temp, "pre bio", "bio")
  temp <- str_replace_all(temp, "mech eng", "me")
  temp <- str_replace_all(temp, "fin. math stats", "financial math & stats")
  temp <- str_replace_all(temp, "soc", "sociology")
  temp <- str_replace_all(temp, "mechanical engineering", "me")
  temp <- str_replace_all(temp, "pre econ accounting", "econ and accounting")
  temp <- str_replace_all(temp, "mathematics and statistics", "math and stats")
  temp <- str_replace_all(temp, "biopsychology", "biopsych")
  temp <- str_replace_all(temp, "sociologyiology", "sociology")
  temp <- str_replace_all(temp, "statistical science", "stats")
  temp <- str_replace_all(temp, "statistics", "stats")
  temp <- str_replace_all(temp, "communication and tmp", "comm")
  temp <- str_replace_all(temp, "chemistry", "chem")
  temp <- str_replace_all(temp, "researcher at cs dept", "cs")
  
  return(temp)
}



#' cleans Strings from the HowFound Column
#' should be used with lapply
#' @param string the string to be cleaned
#' @return the cleaned string
#' @noRd
cleanFound <- function(string){
  found <- tolower(string)
  
  #' Helper function that checks replaces a string with word if that word exists somewhere in the string
  #' @param replace the string to be replaced
  #' @noRd
  simplify <- function(replace){
    return(ifelse(grepl(replace, found), replace, found))
  }
  
  found <- simplify('reddit')
  found <- simplify('facebook')
  found <- simplify('org fair')
  found <- simplify('friend')
  
  found <- str_trim(found)
  
  #edge cases
  found <- str_replace_all(found, "redddit", "reddit")
  found <- str_replace_all(found, "wechat", "facebook")
  found <- str_replace_all(found, "roommate", "friend")
  found <- str_replace_all(found, "\\(edited\\)", "")
  
  found <- str_replace_all(found, "none given", "other")
  found <- str_replace_all(found, "google", "other")
  found <- str_replace_all(found, "previous user", "other")
  
  return(found)
}



#' Reads introductions.csv and returns a dataframe with the data already cleaned
#' @return Clean dataframe of introduction data
get_intro_data <- function(){
  #read data from the file
  data = read.csv('./lib/introductions.csv')
  
  #cleans the data
  data[1] <- lapply(data[1], cleanYearAndSchool)
  data[2] <- lapply(data[2], cleanYearAndSchool)
  data[3] <- lapply(data[3], cleanMajor)
  data[5] <- lapply(data[5], cleanFound)
  
  data$Year[data$Year == ""] <- NA #annoying edge case
  
  #give the data better column names
#  colnames(data) <- c("School", "Year", "Major", "ReasonJoin", "HowFound")
  
  data = na.omit(data)
  
  return(data)
}



#writes all unique majors to a csv file so that they can be categorized by hand
#write.csv(unique(data$Major), './lib/majors.csv')


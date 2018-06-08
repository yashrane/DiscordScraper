library(rsconnect)
files_to_publish = c('lib/', 'app.R', 
                     'loadIntroData.R', 'loadMessageData.R',
                     'makeIntroPlots.R')  
wd = 'C:/Users/yashr/Documents/Random Projects/DiscordScraper/plots'
name = "DiscordData"

deployApp(appFiles=files_to_publish, appName=name, appDir = wd, launch.browser = FALSE)

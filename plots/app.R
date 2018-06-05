#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#



library(shiny)
source("makeIntroPlots.R")
source("loadMessageData.R")

#library(rsconnect)




# Define UI for application that draws a histogram
ui <- fluidPage(
  
  # Application title
  titlePanel("Demographic Data"),
  
  # fluidRow(
  #   column(8,
  #     plotOutput("messagePlots")
  #   ),
  #   
  #   column(4,
  #          plotOutput("introPlots")
  #   )
  #   
  #   
  # )
  
  # Sidebar with a slider input for number of bins
  sidebarLayout(
    uiOutput("out1"),

    # Show a plot of the generated distribution
    mainPanel(

      tabsetPanel(id="tabs",
                  tabPanel("Notifications", htmlOutput("notifications")),
                  tabPanel("Usage", plotOutput("messagePlots"))
      )

    )
  )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  # output$out1 <- renderUI({
  #   type <- input$tabs
  #   if(identical(type, "Demographics")){
  #     panel <-sidebarPanel(
  #               radioButtons("Type", 
  #                  h3("Choose the type of plot"), 
  #                  choices = list("Major" = 1, "Year and How They Found the Server" = 2), 
  #                  selected = 1))
  #   }
  #   if(identical(type, "Usage")){
  #     panel <-sidebarPanel(
  #       radioButtons("Type", 
  #                    h3("Choose the type of plot"), 
  #                    choices = list("Overview" = 1, "Average Day" = 2), 
  #                    selected = 1))
  #   }
  #   
  #   return(panel)
  # })
  
  
  
  output$messagePlots <- renderPlot({
    choice <- 1
    if(is.null(choice)){
      return()
    }
    if(choice == 1){
      type_str <- "Overview"
    }
    if(choice == 2){
      type_str <- "Day"
    }
    
    make_message_graphs(type_str)
  })
  
  output$introPlots <- renderPlot({
    
    choice <- 1
    if(is.null(choice)){
      return()
    }
    if(choice == 1){
      type_str <- "major"
    }
    else if(choice == 2){
      type_str <- "year/found"
    }
    
    make_plot(type_str)
  })
  
  output$notifications <- renderPrint({
    
    #figure out how to center alight everything?
    #see if its worth going for broke and switching to plotly
    
    reg_info <- usage_info()
    print_formatted<-function(x, type){
      if(type == "add"){
        text <- span(h4(x), style="color:darkgray")
      }
      else if (type == "remove"){
        text<- span(h4(x), style="color:cornflowerblue")
      }
      print(text)
    }
    
    print(h2("New Regulars"))
    lapply(reg_info$add, print_formatted, "add")
    print(br())
    
    #look into reactive text components
    if(length(reg_info$remove) > 5){
      print(h2(paste0("New Regular Mortis(",length(reg_info$remove),")")))
    }
    else{
      print(h2("New Regular Mortis"))
      lapply(reg_info$remove, print_formatted, "remove")
    }
    
    return(invisible("placeholder"))
  })
  
  
}

# Run the application 
shinyApp(ui = ui, server = server)


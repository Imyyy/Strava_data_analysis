setwd("~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Projects_for_fun/Strava/Data/export_45393409/activities/")
library(tidyverse)
library(devtools)
library(gtools)
library(mapproj)
library(dpylr)

# install_github("marcusvolz/strava") # devtools::
library(strava) # Now loads! the key seemed to be removing the ::devtools

data <- process_data('2656327997.gpx') # strava::?

# Looking at this tutorial to read the GPX files 
# https://rcrastinate.blogspot.com/2014/09/stay-on-track-plotting-gps-tracks-with-r.html

library(XML)
library(rJava) # installed to install the next one
library(OpenStreetMap)
library(lubridate)
library(ggplot2)

## LOADING CSVs
# Trying to load some of the csvs that are given, before moving on to the activity data

path <- "/Users/imytest/Library/Mobile Documents/com~apple~CloudDocs/Documents/Projects_for_fun/Strava/Data/export_45393409/" 
# file <- 'activities.csv'
print(paste(path,'activities.csv', sep="")) # sep = ""

activities <- read.csv(paste(path,'activities.csv', sep="")) # the only really useful csv
challenges <- read.csv(paste(path,'challenges.csv', sep=""))
segments <- read.csv(paste(path,'segments.csv', sep="")) # only lists need for mead

head(activities)
colnames(activities)

ggplot(data = activities, aes(x=Activity.Type)) + 
  geom_bar(fill='#009E73') + 
  labs(x = "Activity", y="Count") +
  theme_classic()

library("tmaptools")
data <- read_GPX(paste(path,'2639213462.gpx',  sep=""))

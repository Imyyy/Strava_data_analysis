library(dplyr)
library(ggplot2)

### Load in summary data
data <- read.csv("../Data/Processed_data/Totals_by_year.csv")

head(data)

data <- subset(data, select = -c(X))


# Filter to only the outdoor
outdoor <- data %>% 
  filter(Type!="StairStepper" & Type!="VirtualRide") %>% 
  rename(Distance.km = Distance..km.)

# Plots -------------------------------------------------------------------

max_dist = round(max(outdoor$Distance.km), -2). # Max dist to nearest 100, for neat plots

ggplot(outdoor, aes(x=Year, y = Distance.km, fill=Type)) + 
  geom_col(position="stack") + 
  scale_fill_brewer(palette = "Pastel1") + 
  theme_linedraw() + 
  labs(title = "Distance by activity per year", x = "Year", y = "Distance (km)") +
  scale_y_continuous(breaks = scales::pretty_breaks(n = max_dist / 200))


library(dplyr)
library(ggplot2)
library(plotly)

### Load in summary data
data <- read.csv("../Data/Processed_data/camino.csv")

head(data)

data <- subset(data, select = -c(X))

data <- data %>% 
  mutate(
  distance_km = distance / 1000, 
  moving_min = moving_time / 60, 
  elapsed_min = elapsed_time / 60,
  camino = if_else(grepl("bonus", name, ignore.case = TRUE), "Finisterre", "Frances"),
  moving_hour = round((moving_min / 60), 1)) # +
  # filter(id != 14456053386) # TODO refilter out monparnasse

# Scatter -----------------------------------------------------------------
# Elapsed time vs moving time
time <- ggplot(data, aes(x=moving_min, y=elapsed_min, col=moving_time, text = paste0(name))) +
  geom_point() +
  theme_bw() +
  labs(x="Move", y="Elapsed") +
  expand_limits(x = 2, y = 3)
ggplotly(time, tooltip = "text"). # Convert to interactive plotly plot with tooltips

# Distance elevation
dist_elev <- ggplot(data, aes(x=distance_km, y=total_elevation_gain, 
                              col=factor(camino), alpha = 0.5, size = moving_hour,
                              text = paste0("Title: ", name, "\nHours: ", round(moving_hour, 1)))) +
  geom_point() + 
  labs(x="Distance (km)", y="Elevation gain (m)") + 
  guides(alpha = "none", col = guide_legend("Camino")) +
  scale_color_manual(
   values = c("Finisterre" = "maroon3", "Frances" = "mediumslateblue"),
   labels = c("Y" = "Frances", "N" = "Finisterre"),
   name = "Camino") +
  theme_bw() + # scale_size(name="Time") +
  expand_limits(x = 2, y = 2) + guides(alpha = "none", size="none")
  # , colour=guide_legend(), size=guide_legend())
ggplotly(dist_elev, tooltip = "text")

# Heartrate dotplot
ggplot(data, aes(x=max_heartrate)) + geom_histogram(bins=50)

ggplot(data) + 
  geom_density(aes(x = max_heartrate, colour = "blue", alpha=0.5)) + 
  geom_density(aes(x = average_heartrate, colour="red", alpha=0.5)) + 
  labs(x = "") +
  guides(alpha="none")

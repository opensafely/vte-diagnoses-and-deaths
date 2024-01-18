library(tidyverse)
library(arrow)
library(janitor)

dataset <- read_csv_arrow("output/dataset.csv.gz")

roundmid_any <- function(x, to = 6) {
  # like round_any, but centers on (integer) midpoint of the rounding points
  ceiling(x / to) * to - (floor(to / 2) * (x != 0))
}

# primary

crosstab1 <- dataset %>%
  mutate(
    primary_before_tf = ifelse(vte_primary_events_before_covid_count > 0, 1, 0),
    primary_after_tf = ifelse(vte_primary_events_after_covid_count > 0, 1, 0),
    secondary_before_tf = ifelse(vte_secondary_admissions_before_covid_count > 0, 1, 0),
    secondary_after_tf = ifelse(vte_secondary_admissions_after_covid_count > 0, 1, 0)
    ) %>%
  group_by(primary_before_tf,
            primary_after_tf,
            secondary_before_tf,
            secondary_after_tf
            ) %>%
  summarise(n = n()) %>%
  mutate(n = roundmid_any(n))

#ggplot(df_primary, aes(x = n)) +
#  geom_histogram(binwidth = 1) +
#  labs(title = "Distribution of primary care VTE diagnoses", x = "Number of primary care diagnoses", y = "Frequency") +
#  theme_minimal()

write_csv(crosstab1, "output/first_crosstab.csv")

library(tidyverse)
library(arrow)
library(janitor)

dataset <- read_csv_arrow("output/dataset.csv.gz")

roundmid_any <- function(x, to = 6) {
  # like round_any, but centers on (integer) midpoint of the rounding points
  ceiling(x / to) * to - (floor(to / 2) * (x != 0))
}

# primary

df_primary <- dataset %>%
  group_by(vte_count_primary_diagnoses) %>%
  summarise(n = n()) %>%
  mutate(n = roundmid_any(n))

ggplot(df_primary, aes(x = n)) +
  geom_histogram(binwidth = 1) +
  labs(title = "Distribution of primary care VTE diagnoses", x = "Number of primary care diagnoses", y = "Frequency") +
  theme_minimal()

write_csv(df_primary, "output/vte_primary_diagnosis_frequency_distribution.csv")
ggsave("output/df_primary_midpoint_rounded.png")

# secondary

df_secondary <- dataset %>%
  group_by(vte_count_secondary_admissions) %>%
  summarise(n = n()) %>%
  mutate(n = roundmid_any(n))

ggplot(df_secondary, aes(x = n)) +
  geom_histogram(binwidth = 1) +
  labs(title = "Distribution of secondary care VTE admissions", x = "Number of secondary care admissions", y = "Frequency") +
  theme_minimal()

write_csv(df_secondary, "output/vte_secondary_admission_frequency_distribution.csv")
ggsave("output/df_secondary_midpoint_rounded.png")

# secondary mb

df_secondary_mb <- dataset %>%
  group_by(vte_count_secondary_admissions) %>%
  summarise(n = n()) %>%
  mutate(n = roundmid_any(n))

ggplot(df_secondary_mb, aes(x = n)) +
  geom_histogram(binwidth = 1) +
  labs(title = "Distribution of secondary care VTE admissions", subtitle = "Using MB's codelist", x = "Number of secondary care admissions", y = "Frequency") +
  theme_minimal()

write_csv(df_secondary_mb, "output/vte_secondary_mb_admission_frequency_distribution.csv")
ggsave("output/df_secondary_mb_midpoint_rounded.png")

# crosstab secondary

df_crosstab <- dataset %>%
  mutate(
    patients_with_primary_diagnosis = ifelse(vte_count_primary_diagnoses > 0, 1, 0),
    patients_with_secondary_admission = ifelse(vte_count_secondary_admissions > 0, 1, 0),
    patients_with_secondary_admission_mb = ifelse(vte_count_secondary_admissions_mb > 0, 1, 0),
    patients_with_any_secondary_admission = ifelse(patients_with_secondary_admission > 0 | patients_with_secondary_admission_mb > 0, 1, 0)
  ) 

crosstab_secondary_codelists <- df_crosstab %>%
  group_by(patients_with_secondary_admission, patients_with_secondary_admission_mb) %>%
  summarise(n=n()) %>%
  ungroup() %>%
  mutate(n = roundmid_any(n), 
         p = round(n/sum(n), 3) %>%
  arrange(desc(p)) 

write_csv(crosstab_secondary_codelists, "output/crosstab_secondary_codelists_midpoint_rounded.csv")

crosstab_primary_secondary <- df_crosstab %>% 
  group_by(patients_with_primary_diagnosis, patients_with_any_secondary_admission) %>%
  summarise(n=n()) %>%
  ungroup() %>%
  mutate(n = roundmid_any(n), 
         p = round(n/sum(n), 3) %>%
  arrange(desc(p)) 

write_csv(crosstab_primary_secondary, "output/crosstab_primary_secondary_midpoint_rounded.csv")

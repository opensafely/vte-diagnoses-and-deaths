from ehrql import Dataset
from ehrql.tables.beta.core import patients
from ehrql.tables.beta.tpp import (
    clinical_events,
    ons_deaths,
    hospital_admissions,
)
from ehrql.codes import CTV3Code
from codelists import (
    codelist_vte_ctv3,
    codelist_vte_icd10,
    codelist_vte_icd10_mb,
)

dataset = Dataset()

start_date_1 = "2018-03-01"
end_date_1 = "2020-02-29"
start_date_2 = "2020-03-01"
end_date_2 = "2022-02-28"

# events ####
vte_primary_events_before_covid = clinical_events.where(
    (clinical_events.ctv3_code.is_in(codelist_vte_ctv3))
    & (clinical_events.date >= start_date_1)
    & (clinical_events.date <= end_date_1)
)

vte_primary_events_after_covid = clinical_events.where(
    (clinical_events.ctv3_code.is_in(codelist_vte_ctv3))
    & (clinical_events.date >= start_date_2)
    & (clinical_events.date <= end_date_2)
)

vte_secondary_admissions_before_covid = hospital_admissions.where(
    hospital_admissions.primary_diagnoses.is_in(codelist_vte_icd10)
    & (hospital_admissions.admission_date >= start_date_1)
    & (hospital_admissions.admission_date >= end_date_1)
)

vte_secondary_admissions_after_covid = hospital_admissions.where(
    hospital_admissions.primary_diagnoses.is_in(codelist_vte_icd10)
    & (hospital_admissions.admission_date >= start_date_2)
    & (hospital_admissions.admission_date >= end_date_2)
)

# any patient who has a diagnosis of VTE in primary or secondary care
# todo: or any patient who has VTE listed as cause of death

dataset.define_population(
    (vte_primary_events_before_covid.exists_for_patient())
    | (vte_primary_events_after_covid.exists_for_patient())
    | (vte_secondary_admissions_before_covid.exists_for_patient()
    | (vte_secondary_admissions_after_covid.exists_for_patient())
))

# primary and secondary care vte events and admissions
dataset.vte_primary_events_before_covid_count = vte_primary_events_before_covid.count_for_patient()
dataset.vte_primary_events_after_covid_count = vte_primary_events_after_covid.count_for_patient()
dataset.vte_secondary_admissions_before_covid_count = vte_secondary_admissions_before_covid.count_for_patient()
dataset.vte_secondary_admissions_after_covid_count = vte_secondary_admissions_after_covid.count_for_patient()

# deaths
dataset.has_died = ons_deaths.exists_for_patient()
dataset.date_of_death = ons_deaths.date
dataset.age_at_death = patients.age_on(ons_deaths.date)

# age and sex
dataset.age_at_study_end = patients.age_on(end_date_2)
dataset.sex = patients.sex

# bmi
dataset.bmi = (
    clinical_events.where(clinical_events.ctv3_code == CTV3Code("22K.."))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .numeric_value
)

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

start_date = "2018-01-01"
end_date = "2022-12-31"

# events ####
vte_primary_events = clinical_events.where(
    (clinical_events.ctv3_code.is_in(codelist_vte_ctv3))
    & (clinical_events.date >= start_date)
    & (clinical_events.date <= end_date)
)

vte_secondary_admissions = hospital_admissions.where(
    hospital_admissions.primary_diagnoses.is_in(codelist_vte_icd10)
).where(hospital_admissions.admission_date.is_on_or_after(start_date))

vte_secondary_admissions_mb = hospital_admissions.where(
    hospital_admissions.primary_diagnoses.is_in(codelist_vte_icd10_mb)
).where(hospital_admissions.admission_date.is_on_or_after(start_date))


# any patient who has a diagnosis of VTE in primary or secondary care
# todo: or any patient who has VTE listed as cause of death
dataset.define_population(
    (vte_primary_events.exists_for_patient())
    | (vte_secondary_admissions.exists_for_patient())
    | (vte_secondary_admissions_mb.exists_for_patient())
)

# primary care vte events
most_recent_vte_primary = vte_primary_events.sort_by(
    vte_primary_events.date
).last_for_patient()
dataset.date_of_last_vte_primary_diagnosis = most_recent_vte_primary.date
dataset.code_of_last_vte_primary_diagnosis = most_recent_vte_primary.ctv3_code
dataset.vte_count_primary_diagnoses = vte_primary_events.count_for_patient()

# vte deaths
dataset.has_died = ons_deaths.exists_for_patient()
most_recent_death_date = ons_deaths.sort_by(ons_deaths.date).last_for_patient()
dataset.date_of_death = most_recent_death_date.date
dataset.age_at_death = patients.age_on(most_recent_death_date.date)

# age and sex
dataset.age_at_last_vte = patients.age_on(most_recent_vte_primary.date)
dataset.sex = patients.sex

# patients with hospital admission code of vte


dataset.first_vte_hospitalisation_date = (
    vte_secondary_admissions.sort_by(hospital_admissions.admission_date)
    .first_for_patient()
    .admission_date
)
dataset.vte_count_secondary_admissions = (
    vte_secondary_admissions.count_for_patient()
)

# patients with hospital admission code of vte (alternative codelist)

dataset.first_vte_hospitalisation_date_mb = (
    vte_secondary_admissions_mb.sort_by(hospital_admissions.admission_date)
    .first_for_patient()
    .admission_date
)

dataset.vte_count_secondary_admissions_mb = (
    vte_secondary_admissions_mb.count_for_patient()
)

# bmi
dataset.bmi = (
    clinical_events.where(clinical_events.ctv3_code == CTV3Code("22K.."))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .numeric_value
)

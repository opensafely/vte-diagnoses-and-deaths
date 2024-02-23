################################################################################
#
# Description: This script provides the formal specification of the study data 
#              that will be extracted from the OpenSAFELY database.
#
# Output: output/dataset_incident_VTE.csv.gz
#
# Author(s): J.Mutio, M Green
# Date last updated: 22/02/2024
#
################################################################################





# IMPORT STATEMENTS ------------------------

# Import tables and Python objects
from ehrql import Dataset, years, days, minimum_of
from ehrql.tables.beta.core import patients
from ehrql.tables.beta.tpp import (
  clinical_events,
  hospital_admissions,
  medications,
  ons_deaths,
  practice_registrations,
)
from ehrql.codes import CTV3Code


# Import codelists
from codelists import (
  codelist_vte_ctv3,
  codelist_vte_icd10_mb,
  codelist_anticoagulant_prescription
)


# Define dates
start_date = "2018-01-01"
end_date = "2022-12-31"




# DEFINE DATASET ------------------------

# Create dataset object for output dataset
dataset = Dataset()


# Population variables

## Patients with a VTE code recorded in their primary care data within study period
vte_primary_care = clinical_events.where((clinical_events.ctv3_code.is_in(codelist_vte_ctv3))
    & (clinical_events.date >= start_date)
    & (clinical_events.date <= end_date))

vte_primary_care_date = vte_primary_care.sort_by(vte_primary_care.date).first_for_patient().date

## Patients with a VTE code in the year prior to their first primary care VTE code in the study period
vte_within_1yr_prior_primary_care = clinical_events.where(
  (clinical_events.ctv3_code.is_in(codelist_vte_ctv3))
  & (clinical_events.date < vte_primary_care_date)
  & (clinical_events.date > vte_primary_care_date - years(1)))

## Patients with a VTE code recorded as primary digasosis in hospital admission within study period
vte_secondary_care = hospital_admissions.where(
  hospital_admissions.primary_diagnoses.is_in(codelist_vte_icd10_mb)).where(
    hospital_admissions.admission_date.is_on_or_after(start_date))

vte_secondary_care_date = vte_secondary_care.sort_by(
  vte_secondary_care.admission_date).first_for_patient().admission_date

## Patients with a VTE code in the year prior to their first secondary care VTE code in the study period
vte_within_1yr_prior_secondary_care = clinical_events.where(
  (clinical_events.ctv3_code.is_in(codelist_vte_ctv3))
  & (clinical_events.date < vte_secondary_care_date)
  & (clinical_events.date > vte_secondary_care_date - years(1)))

## Patients with a prescription for an anticoagulant between 15 days before and 90 days after their VTE code
vte_diagnosis_date = minimum_of(vte_primary_care_date, vte_secondary_care_date)

anticoagulant_prescription = medications.where(
  medications.dmd_code.is_in(codelist_anticoagulant_prescription)).where(
  medications.date.is_on_or_between(vte_diagnosis_date - days(15), vte_diagnosis_date + days(90))).exists_for_patient()
    
## Death within 30 days of VTE code
died_within_30_days = ons_deaths.date.is_on_or_between(
    vte_diagnosis_date, vte_diagnosis_date + days(30))

## Patients registered at the time of their VTE
registered_at_VTE = practice_registrations.for_patient_on(vte_diagnosis_date).exists_for_patient()

## Patients alive at the time of their VTE
alive_at_VTE = (patients.date_of_death.is_after(vte_diagnosis_date) | patients.date_of_death.is_null())

## Patients with 1 year of follow up prior to VTE
has_follow_up_previous_12months = practice_registrations.where(
    practice_registrations.start_date.is_on_or_before(vte_diagnosis_date - years(1))
    & (practice_registrations.end_date.is_after(vte_diagnosis_date) | practice_registrations.end_date.is_null())).exists_for_patient()

# Define dataset as;
#       - Any patient who has a diagnosis of VTE in primary or secondary care in the study period 
#       - (todo: or any patient who has VTE listed as cause of death)?
#       - Alive and registered on VTE date 
#       - 1 year of follow up prior to VTE
#       - Excluding those with a VTE diagnosis codes within one year of the first VTE code in the study period
#       AND
#       - Prescription for an anticoagulant between 15 days before and 90 days after the VTE diagnosis
#           OR
#       - a date of death within 30 days of the event


dataset.define_population(
  (vte_primary_care.exists_for_patient() & ~vte_within_1yr_prior_primary_care.exists_for_patient())
  & (vte_secondary_care.exists_for_patient() & ~vte_within_1yr_prior_secondary_care.exists_for_patient())
  & registered_at_VTE
  & alive_at_VTE
  & has_follow_up_previous_12months
  & (anticoagulant_prescription | died_within_30_days)
  )


# Primary care VTE information

## Date of primary VTE
dataset.date_of_vte_primary_diagnosis = vte_primary_care_date
dataset.date_of_vte_secondary_diagnosis = vte_secondary_care_date


# Demographic variables

## Age (on VTE date)
dataset.age_at_vte = patients.age_on(vte_diagnosis_date)

## Sex
dataset.sex = patients.sex




# (TO DO - from application)
## BMI, ethnicity, IMD, care home status, Geographical location, Comorbidities (including LD),
## Covid test status/Covid vaccination status, 
## Healthcare encounters close to death including whether these were in primary and/or secondary care,
## If possible, include whether the patient had been admitted on a virtual ward close to death
## Outcome - VTE-related death

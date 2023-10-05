from ehrql import Dataset, codelist_from_csv
from ehrql.tables.beta.core import patients
from ehrql.tables.beta.tpp import clinical_events, ons_deaths, hospital_admissions, medications
from ehrql.codes import CTV3Code

dataset = Dataset()

start_date = "2018-01-01"
end_date = "2022-12-31"

# importing codelists ####

codelist_vte_ctv3 = codelist_from_csv(
    "codelists/opensafely-venous-thromboembolic-disease.csv",
    column="CTV3Code", # for primary care
)

codelist_vte_icd10 = codelist_from_csv(
    "codelists/opensafely-venous-thromboembolic-disease-hospital.csv",
    column="ICD_code" # for secondary care
)

codelist_vte_icd10_mb = codelist_from_csv(
    "codelists/user-matthewberesford92-venous-thromboembolism.csv",
    column="code" # for secondary care to compare
)

codelist_acute_infection_snomed = codelist_from_csv(
        "codelists/user-jon_massey-serious_acute_infection.csv",
        column="code"
)

codelist_coronary_heart_disease_snomed = codelist_from_csv(
        "codelists/nhsd-primary-care-domain-refsets-chd_cod.csv",
        column = "code"
)

codelist_coronary_heart_disease_icd = codelist_from_csv(
        "codelists/user-matthewberesford92-coronary-heart-disease-icd10.csv",
        column = "code"        
)

codelist_heart_failure_snomed_1 = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hf_cod.csv",
    column = "code"    
)

codelist_heart_failure_snomed_2 = codelist_from_csv(
    "codelists/pincer-hf.csv",
    column = "code"
)

codelist_heart_failure_icd = codelist_from_csv(
    "codelists/user-matthewberesford92-heart-failure-icd-10.csv",
    column = "code"    
)

codelist_respiratory_snomed = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-resp_cov.csv",
    column = "code"    
)

codelist_respiratory_icd = codelist_from_csv(
    "codelists/user-matthewberesford92-chronic-respiratory-disease-icd10.csv",
    column = "code"    
)

#codelist_thrombophilia_snomed = codelist_from_csv(
#    "https://phenotypes.healthdatagateway.org/concepts/C2905/version/7425/detail/",
#    column = ""    
#)

codelist_pregnancy_snomed = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-c19preg_cod.csv",
    column = "code"    
)

codelist_hormonal_contraception_dmd = codelist_from_csv(
    "codelists/user-matthewberesford92-oestrogen-based-drugs-excluding-topical-preparations.csv",
    column = "code"    
)

codelist_ethnicity = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    column = "Code"
)

# events ####

vte_primary_events = clinical_events.where(
    (clinical_events.ctv3_code.is_in(codelist_vte_ctv3))
    & (clinical_events.date >= start_date)
    & (clinical_events.date <= end_date)
)

# any patient who has a diagnosis of VTE in primary or secondary care
# or any patient who has VTE listed as cause of death
dataset.define_population(vte_primary_events.exists_for_patient())

most_recent_vte = vte_primary_events.sort_by(vte_primary_events.date).last_for_patient()
dataset.date_of_last_vte = most_recent_vte.date
dataset.code_of_last_vte = most_recent_vte.ctv3_code

# vte deaths
dataset.has_died = ons_deaths.exists_for_patient()
most_recent_death_date = ons_deaths.sort_by(ons_deaths.date).last_for_patient()
dataset.date_of_death = most_recent_death_date.date
dataset.age_at_death = patients.age_on(most_recent_death_date.date)

# age and sex
dataset.age_at_last_vte = patients.age_on(most_recent_vte.date)
dataset.sex = patients.sex

# ethnicity 

# patients with hospital admission code of vte
dataset.first_vte_hospitalisation_date = hospital_admissions.where(
        hospital_admissions.primary_diagnoses.is_in(codelist_vte_icd10)
).where(
        hospital_admissions.admission_date.is_on_or_after(start_date)
).sort_by(
        hospital_admissions.admission_date
).first_for_patient().admission_date

# mb -- patients with hospital admission code of vte
dataset.first_vte_hospitalisation_date_mb = hospital_admissions.where(
        hospital_admissions.primary_diagnoses.is_in(codelist_vte_icd10_mb)
).where(
        hospital_admissions.admission_date.is_on_or_after(start_date)
).sort_by(
        hospital_admissions.admission_date
).first_for_patient().admission_date

# bmi
dataset.bmi = clinical_events.where(
    clinical_events.ctv3_code == CTV3Code("22K..")
    ).sort_by(clinical_events.date
    ).last_for_patient().numeric_value
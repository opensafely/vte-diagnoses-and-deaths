from ehrql import Dataset, codelist_from_csv
from ehrql.tables.beta.core import patients
from ehrql.tables.beta.tpp import clinical_events, ons_deaths, hospital_admissions

dataset = Dataset()

start_date = "2018-01-01"
end_date = "2022-12-31"

vte_codes_primary = codelist_from_csv(
    "codelists/opensafely-venous-thromboembolic-disease.csv",
    column="CTV3Code",
)
vte_codes_secondary = codelist_from_csv(
    "codelists/opensafely-venous-thromboembolic-disease-hospital.csv",
    column="ICD_code"
)

vte_primary_events = clinical_events.where(
    (clinical_events.ctv3_code.is_in(vte_codes_primary))
    & (clinical_events.date >= start_date)
    & (clinical_events.date <= end_date)
)


# any patient who has a diagnosis of VTE in primary or secondary care
# or any patient who has VTE listed as cause of death
dataset.define_population(vte_primary_events.exists_for_patient())

most_recent_vte = vte_primary_events.sort_by(vte_primary_events.date).last_for_patient()
dataset.date_of_last_vte = most_recent_vte.date
dataset.code_of_last_vte = most_recent_vte.ctv3_code
dataset.age_at_last_vte = patients.age_on(most_recent_vte.date)

dataset.has_died = ons_deaths.exists_for_patient()
most_recent_death_date = ons_deaths.sort_by(ons_deaths.date).last_for_patient()
dataset.date_of_death = most_recent_death_date.date
dataset.age_at_death = patients.age_on(most_recent_death_date.date)

# patients with hospital admission code of vte
dataset.first_vte_hospitalisation_date = hospital_admissions.where(
        hospital_admissions.primary_diagnoses.is_in(vte_codes_secondary)
).where(
        hospital_admissions.admission_date.is_on_or_after(start_date)
).sort_by(
        hospital_admissions.admission_date
).first_for_patient().admission_date
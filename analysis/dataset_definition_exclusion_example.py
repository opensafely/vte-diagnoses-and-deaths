from ehrql import Dataset
from ehrql.tables.beta.tpp import (
    clinical_events,
    hospital_admissions,
)
from ehrql.codes import CTV3Code
from codelists import codelist_vte_ctv3, codelist_vte_icd10

dataset = Dataset()

period_1_start_date = "2018-01-01"
period_1_end_date = "2020-12-31"

period_2_start_date = "2021-01-01"
period_2_end_date = "2022-12-31"

# events
vte_primary_events = clinical_events.where(
    (clinical_events.ctv3_code.is_in(codelist_vte_ctv3))
)

vte_secondary_admissions = hospital_admissions.where(
    hospital_admissions.primary_diagnoses.is_in(codelist_vte_icd10)
)

inclusion = (
    vte_primary_events.where(
        (vte_primary_events.date >= period_1_start_date)
        & (vte_primary_events.date <= period_1_end_date)
    ).exists_for_patient()
    | vte_secondary_admissions.where(
        (vte_secondary_admissions.admission_date >= period_1_start_date)
        & (vte_secondary_admissions.admission_date <= period_1_end_date)
    ).exists_for_patient()
)

exclusion = (
    vte_primary_events.where(
        (vte_primary_events.date >= period_2_start_date)
        & (vte_primary_events.date <= period_2_end_date)
    ).exists_for_patient()
    | vte_secondary_admissions.where(
        (vte_secondary_admissions.admission_date >= period_2_start_date)
        & (vte_secondary_admissions.admission_date <= period_2_end_date)
    ).exists_for_patient()
)


# any patient who has a diagnosis of VTE in primary or secondary care
# in period 1 but not in period 2
dataset.define_population(inclusion & ~exclusion)

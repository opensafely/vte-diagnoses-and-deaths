from ehrql import codelist_from_csv

# importing codelists ####

codelist_vte_ctv3 = codelist_from_csv(
    "codelists/opensafely-venous-thromboembolic-disease.csv",
    column="CTV3Code",  # for primary care
)

codelist_vte_icd10 = codelist_from_csv(
    "codelists/opensafely-venous-thromboembolic-disease-hospital.csv",
    column="ICD_code",  # for secondary care
)

codelist_vte_icd10_mb = codelist_from_csv(
    "codelists/user-matthewberesford92-venous-thromboembolism.csv",
    column="code",  # for secondary care to compare
)

codelist_acute_infection_snomed = codelist_from_csv(
    "codelists/user-jon_massey-serious_acute_infection.csv", column="code"
)

codelist_acute_infection_icd = codelist_from_csv(
    "codelists/user-matthewberesford92-serious-acute-infection.csv",
    column="code",
)

codelist_coronary_heart_disease_snomed = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-chd_cod.csv", column="code"
)

codelist_coronary_heart_disease_icd = codelist_from_csv(
    "codelists/user-matthewberesford92-coronary-heart-disease-icd10.csv",
    column="code",
)

codelist_heart_failure_snomed_1 = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hf_cod.csv", column="code"
)

codelist_heart_failure_snomed_2 = codelist_from_csv(
    "codelists/pincer-hf.csv", column="code"
)

codelist_heart_failure_icd = codelist_from_csv(
    "codelists/user-matthewberesford92-heart-failure-icd-10.csv", column="code"
)

codelist_respiratory_snomed = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-resp_cov.csv", column="code"
)

codelist_respiratory_icd = codelist_from_csv(
    "codelists/user-matthewberesford92-chronic-respiratory-disease-icd10.csv",
    column="code",
)

# codelist_thrombophilia_snomed = codelist_from_csv(
#    "https://phenotypes.healthdatagateway.org/concepts/C2905/version/7425/detail/",
#    column = ""
# )

codelist_pregnancy_snomed = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-c19preg_cod.csv", column="code"
)

codelist_hormonal_contraception_dmd = codelist_from_csv(
    "codelists/user-matthewberesford92-oestrogen-based-drugs-excluding-topical-preparations.csv",
    column="code",
)

codelist_ethnicity = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv", column="Code"
)

codelist_oral_anticoagulation = codelist_from_csv(
    "codelists/user-matthewberesford92-oral-anticoagulation-used-for-treatment-of-vte-in-primary-care-uk-dmd-dmd.csv",
    column="dmd_id"
)

codelist_anticoagulation_taken = codelist_from_csv(
    "codelists/user-matthewberesford92-anticoagulation-taken-for-vte-dmd.csv",
    column="dmd_id"
)

codelist_anticoagulant_prescription = (codelist_oral_anticoagulation + codelist_anticoagulation_taken)

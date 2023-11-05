import pandas as pd


def redact(x):
    return x if x == 0 or x > 7 else "redacted"


dataset = pd.read_csv("output/dataset.csv.gz")

vte_code_cols = [
    c
    for c in dataset.columns
    if c.startswith("vte_primary_events") and c.endswith("code")
]

results = {c: dataset[c].value_counts() for c in vte_code_cols}

for vte_column, code_counts in results.items():
    code_counts = code_counts.apply(redact)
    code_counts.to_csv(f"output/{vte_column}.csv", header=False, index=True)

from dataset_definition import dataset, codelist_vte_ctv3, vte_primary_events


# function to "pivot" clincal event codes
def pivot_events(dataset, codelist, events, variable_base_name, n):
    events = events.sort_by(events.date)
    for i in range(1, n + 1):
        varname = f"{variable_base_name}_{i}"
        event = events
        if i > 1:
            event = event.where(
                events.date > dataset.__getattr__(f"{variable_base_name}_{i-1}_date")
            )
        event = event.first_for_patient()
        dataset.__setattr__(f"{varname}_date", event.date)
        dataset.__setattr__(f"{varname}_code", event.ctv3_code)


# get the first five primary care VTE dianosis codes & dates for each patient
pivot_events(dataset, codelist_vte_ctv3, vte_primary_events, "vte_primary_events", 5)

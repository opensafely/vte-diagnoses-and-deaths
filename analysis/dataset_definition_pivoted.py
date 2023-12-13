from dataset_definition import dataset, vte_primary_events


# function to "pivot" n clincal event codes and dates into
# a single row per patient structure
def pivot_events(dataset, events, variable_base_name, n):
    # ensure events are in date order
    events = events.sort_by(events.date)

    # loop, increment the index up until n
    for i in range(1, n + 1):
        # create a base variable name that includes the index
        varname = f"{variable_base_name}_{i}"
        event = events
        # for everything other than the first event, filter to events
        # later than the previous event
        if i > 1:
            event = event.where(
                events.date > dataset.__getattr__(f"{variable_base_name}_{i-1}_date")
            )
        # take the first eligible event for each patient
        event = event.first_for_patient()
        # add the code and date of that event to the dataset
        dataset.add_column(f"{varname}_date", event.date)
        dataset.add_column(f"{varname}_code", event.ctv3_code)


# get the first five primary care VTE dianosis codes & dates for each patient
pivot_events(dataset, vte_primary_events, "vte_primary_events", 5)

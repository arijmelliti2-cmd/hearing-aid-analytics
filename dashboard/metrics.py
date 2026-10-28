def weighted_average(data, value_column):
    """Calculate an event-weighted average from aggregated data."""
    total_events = data["total_events"].sum()

    if total_events <= 0:
        return 0.0

    weighted_sum = (
        data[value_column] * data["total_events"]
    ).sum()

    return float(weighted_sum / total_events)


def weighted_percentage(data, percentage_column):
    """Calculate an event-weighted percentage from aggregated data."""
    total_events = data["total_events"].sum()

    if total_events <= 0:
        return 0.0

    weighted_sum = (
        data[percentage_column] * data["total_events"]
    ).sum()

    return float(weighted_sum / total_events)
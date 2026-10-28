import pandas as pd
import pytest

from metrics import weighted_average, weighted_percentage


def test_weighted_average_uses_event_counts():
    data = pd.DataFrame({
        "total_events": [10, 100],
        "avg_feedback_rating": [2.0, 4.0],
    })

    result = weighted_average(data, "avg_feedback_rating")

    expected = (10 * 2.0 + 100 * 4.0) / 110

    assert result == pytest.approx(expected)


def test_weighted_percentage_uses_event_counts():
    data = pd.DataFrame({
        "total_events": [10, 100],
        "loud_environment_pct": [50.0, 10.0],
    })

    result = weighted_percentage(data, "loud_environment_pct")

    expected = (10 * 50.0 + 100 * 10.0) / 110

    assert result == pytest.approx(expected)


def test_weighted_average_returns_zero_for_empty_data():
    data = pd.DataFrame({
        "total_events": [],
        "avg_feedback_rating": [],
    })

    assert weighted_average(data, "avg_feedback_rating") == 0.0


def test_weighted_percentage_returns_zero_for_zero_events():
    data = pd.DataFrame({
        "total_events": [0, 0],
        "loud_environment_pct": [50.0, 20.0],
    })

    assert weighted_percentage(data, "loud_environment_pct") == 0.0
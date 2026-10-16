
select *
from {{ ref('agg_hearing_aid_feedback') }}
where
    total_events <= 0
    or avg_feedback_rating < 1
    or avg_feedback_rating > 5
    or loud_environment_pct < 0
    or loud_environment_pct > 100
    or low_feedback_in_loud_environment_pct < 0
    or low_feedback_in_loud_environment_pct > 100

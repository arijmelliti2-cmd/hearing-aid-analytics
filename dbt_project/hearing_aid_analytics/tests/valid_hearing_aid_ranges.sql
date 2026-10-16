
select *
from {{ ref('stg_hearing_aid_events') }}
where
    feedback_rating < 1
    or feedback_rating > 5
    or battery_pct < 0
    or battery_pct > 100
    or environment_noise_db < 0

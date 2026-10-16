
with events as (

    select *
    from {{ ref('fct_hearing_aid_events') }}

),

aggregated as (

    select
        device_model,
        activity,

        count(*) as total_events,

        round(avg(feedback_rating), 2)
            as avg_feedback_rating,

        count(*) filter (
            where feedback_rating <= 2
        ) as low_feedback_events,

        count(*) filter (
            where battery_pct < 20
        ) as low_battery_events,

        round(
            100.0 * count(*) filter (
                where noise_category = 'Loud'
            ) / nullif(count(*), 0),
            2
        ) as loud_environment_pct,

        round(
            100.0 * count(*) filter (
                where low_feedback_in_loud_environment
            ) / nullif(count(*), 0),
            2
        ) as low_feedback_in_loud_environment_pct

    from events

    group by
        device_model,
        activity

)

select *
from aggregated


with events as (

    select *
    from {{ ref('stg_hearing_aid_events') }}

),

enriched as (

    select
        event_id,
        user_id,
        event_timestamp,
        cast(event_timestamp as date) as event_date,

        environment_noise_db,
        activity,
        battery_pct,
        volume_level,
        noise_reduction_level,
        feedback_rating,
        device_model,

        case
            when environment_noise_db < 40 then 'Quiet'
            when environment_noise_db < 70 then 'Moderate'
            else 'Loud'
        end as noise_category,

        case
            when battery_pct < 20 then 'Low'
            when battery_pct < 50 then 'Medium'
            else 'Healthy'
        end as battery_status,

        case
            when feedback_rating <= 2 then 'Poor'
            when feedback_rating = 3 then 'Average'
            else 'Good'
        end as feedback_category

    from events

)

select *
from enriched

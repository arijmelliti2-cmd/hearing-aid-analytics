
with events as (

    select *
    from {{ ref('int_hearing_aid_events') }}

),

final as (

    select
        event_id,
        user_id,
        event_timestamp,
        event_date,
        device_model,
        activity,

        environment_noise_db,
        noise_category,

        battery_pct,
        battery_status,

        volume_level,
        noise_reduction_level,

        feedback_rating,
        feedback_category,

        case
            when noise_category = 'Loud'
                and feedback_rating <= 2
            then true
            else false
        end as low_feedback_in_loud_environment

    from events

)

select *
from final

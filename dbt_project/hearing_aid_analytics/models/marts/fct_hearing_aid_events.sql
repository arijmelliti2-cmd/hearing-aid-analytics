
with events as (
    select *
    from {{ ref('int_hearing_aid_events') }}
),

devices as (
    select device_key, device_model
    from {{ ref('dim_device') }}
),

activities as (
    select activity_key, activity
    from {{ ref('dim_activity') }}
),

final as (
    select
        events.event_id,
        events.user_id,
        events.event_timestamp,
        events.event_date,

        devices.device_key,
        events.device_model,

        activities.activity_key,
        events.activity,

        events.environment_noise_db,
        events.noise_category,
        events.battery_pct,
        events.battery_status,
        events.volume_level,
        events.noise_reduction_level,
        events.feedback_rating,
        events.feedback_category,

        case
            when events.noise_category = 'Loud'
                and events.feedback_rating <= 2
            then true
            else false
        end as low_feedback_in_loud_environment

    from events
    left join devices
        on events.device_model = devices.device_model
    left join activities
        on events.activity = activities.activity
)

select * from final

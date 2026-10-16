

with source as (

    select *
    from {{ ref('hearing_aid_events') }}

),

cleaned as (

    select
        trim(event_id) as event_id,
        trim(user_id) as user_id,
        cast(event_timestamp as timestamp) as event_timestamp,
        cast(environment_noise_db as integer) as environment_noise_db,
        lower(trim(activity)) as activity,
        cast(battery_pct as integer) as battery_pct,
        cast(volume_level as integer) as volume_level,
        cast(noise_reduction_level as integer) as noise_reduction_level,
        cast(feedback_rating as integer) as feedback_rating,
        trim(device_model) as device_model

    from source

)

select *
from cleaned

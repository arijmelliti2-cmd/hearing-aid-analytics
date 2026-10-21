
with devices as (
    select distinct device_model
    from {{ ref('stg_hearing_aid_events') }}
)

select
    md5(device_model) as device_key,
    device_model
from devices

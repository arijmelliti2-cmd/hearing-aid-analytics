
with activities as (
    select distinct activity
    from {{ ref('stg_hearing_aid_events') }}
)

select
    md5(activity) as activity_key,
    activity,
    case
        when activity in ('walking', 'commuting')
            then 'Mobile'
        when activity in ('sitting', 'working')
            then 'Stationary'
        else 'Other'
    end as activity_group
from activities

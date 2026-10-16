
select
    device_model,
    activity,
    count(*) as row_count
from {{ ref('agg_hearing_aid_feedback') }}
group by
    device_model,
    activity
having count(*) > 1

with orders as (

    select * from {{ ref('stg_orders') }}
    where order_status not in ('canceled', 'unavailable')

),

order_revenue as (

    select
        order_id,
        sum(price + freight_value) as order_value
    from {{ ref('stg_order_items') }}
    group by 1

),

order_reviews as (

    select
        order_id,
        avg(review_score) as review_score
    from {{ ref('stg_reviews') }}
    group by 1

),

joined as (

    select
        o.order_id,
        o.customer_id,
        date_trunc('week', o.order_purchase_at) as order_week,
        coalesce(r.order_value, 0) as order_value,
        rv.review_score,
        case
            when o.delivered_at is not null and o.estimated_delivery_at is not null
                and o.delivered_at > o.estimated_delivery_at
            then 1 else 0
        end as is_late,
        case
            when o.delivered_at is not null
            then date_diff('day', o.order_purchase_at, o.delivered_at)
        end as delivery_days
    from orders o
    left join order_revenue r on o.order_id = r.order_id
    left join order_reviews rv on o.order_id = rv.order_id

)

select
    order_week,
    count(distinct order_id) as order_count,
    count(distinct customer_id) as unique_customers,
    round(sum(order_value), 2) as gross_revenue,
    round(sum(order_value) / nullif(count(distinct order_id), 0), 2) as avg_order_value,
    round(avg(review_score), 2) as avg_review_score,
    round(100.0 * sum(is_late) / nullif(count(*), 0), 2) as pct_late_deliveries,
    round(avg(delivery_days), 1) as avg_delivery_days
from joined
group by 1
order by 1

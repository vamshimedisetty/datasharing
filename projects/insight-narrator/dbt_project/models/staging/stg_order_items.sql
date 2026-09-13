select
    order_id,
    order_item_id,
    product_id,
    seller_id,
    price,
    freight_value
from {{ source('raw', 'order_items') }}

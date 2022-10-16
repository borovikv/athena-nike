with customers as (
    select customer_id, name
    from dims.customer
    where country = '{{country}}'
),
products as (
    select product_id, product_name
    from dims.product
    where category = 'Magic'
),
result as (
    select c.name, t.purchase_date, p.product_name, count(*) as items
    from facts.transactions as t
    inner join customers as c on t.customer_id = c.customer_id
    inner join products as p on t.product_id = p.product_id
    group by 1, 2, 3
)
select * from result

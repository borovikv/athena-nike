from tests.fixtures import dims, facts

TABLES = [dims.customer, dims.product, facts.transactions]

SCENARIO = 'sqls/example.sql'

SPECS = dict(
    run_customers=dict(
        scenario=SCENARIO,
        description="""
            Given 2 customers, one from UK and one from US
            When selecting customers
            Only customers from UK are selected
        """,
        tables=TABLES,
        given={
            'dims.customer': [
                {'customer_id': 1, 'name': 'John', 'country': 'UK'},
                {'customer_id': 1, 'name': 'Paul', 'country': 'FR'},
            ]
        },
        params={'country': 'UK'},
        run='customers',
        expected=[{'customer_id': 1, 'name': 'John'}]
    ),

    run_products=dict(
        scenario=SCENARIO,
        description="""
            Given 2 products, only one is from required category
            When selecting customers
            Only products which have correct category will be selected
        """,
        tables=TABLES,
        given={
            'dims.product': [
                {'product_id': 1, 'product_name': 'Wand', 'category': 'Magic'},
                {'product_id': 2, 'product_name': 'Phone', 'category': 'Electronics'},
            ]
        },
        run='products',
        expected=[{'product_id': 1, 'product_name': 'Wand'}]
    )
)

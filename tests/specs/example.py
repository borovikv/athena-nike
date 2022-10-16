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
            When selecting products
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
    ),

    purchase_non_magical_=dict(
        scenario=SCENARIO,
        when='no magical objects where bought',
        tables=TABLES,
        given={
            'dims.customer': [{'customer_id': 1, 'name': 'John', 'country': 'UK'}],
            'dims.product': [
                {'product_id': 2, 'product_name': 'Spell book', 'category': 'Non Magic'}
            ],
            'facts.transactions': [
                {'product_id': 2, 'customer_id': 1, 'purchase_date': '2022-01-01'},
            ]
        },
        params={'country': 'UK'},
        run='result',
        expected=[]
    )
)

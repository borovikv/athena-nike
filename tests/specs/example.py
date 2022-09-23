import tests.fixtures as f

TABLES = [f.dims().customer, f.dims().products, f.facts().transactions]

SCENARIO = 'sqls/example.sql'

SPECS = [
    dict(
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
        run='customers',
        expected=[{'customer_id': 1, 'name': 'John'}]

    )
]

import functools
import os.path

import pytest

from tests.specs_loader import spec_parameters, get_all_specs
from tests.sql import SpecExecutor
from toolbox.sql_utils import get_query
from tests.fixtures import dims, facts


def run_spec(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        spec = f(*args, **kwargs)
        execute = SpecExecutor(spec)
        query_path = os.path.join(*list(filter(bool, [spec.get('path'), spec['scenario']])))
        sql = get_query(query_path, **spec.get('params', {}))

        result = execute(sql, order_by=spec.get('order_by'), cte=spec['run'])

        expected = spec['expected']
        assert result == expected

    return inner


SPECS = get_all_specs('tests.specs')


@pytest.mark.parametrize(**spec_parameters(SPECS))
@run_spec
def test_spec(spec_name, spec, run_name):
    if not (run_name == 'all' or spec_name == run_name):
        # to run specific spec execute make test file=tests/test_sqls.py::test_spec run_name=run_customers
        pytest.skip("unsupported configuration")
    return spec


@run_spec
def test_customers():
    """
    Given 2 customers, one from UK and one from US
    When selecting customers
    Only customer from UK is selected
    """
    return dict(
        scenario='sqls/example.sql',
        tables=[dims.customer, dims.product, facts.transactions],
        given={
            'dims.customer': [
                {'customer_id': 1, 'name': 'John', 'country': 'UK'},
                {'customer_id': 1, 'name': 'Paul', 'country': 'FR'},
            ]
        },
        params={'country': 'UK'},
        run='customers',
        expected=[{'customer_id': 1, 'name': 'John'}]
    )


@run_spec
def test_result():
    """
    Given a customer from UK who bought 2 spell books on first day and 1 on second day
    When calculating result
    Then all purchases are properly accounted for the user
    """
    return dict(
        scenario='sqls/example.sql',
        tables=[dims.customer, dims.product, facts.transactions],
        given={
            'dims.customer': [{'customer_id': 1, 'name': 'John', 'country': 'UK'}],
            'dims.product': [{'product_id': 1, 'product_name': 'Spell book', 'category': 'Magic'}],
            'facts.transactions': [
                {'product_id': 1, 'customer_id': 1, 'purchase_date': '2022-01-01'},
                {'product_id': 1, 'customer_id': 1, 'purchase_date': '2022-01-01'},
                {'product_id': 1, 'customer_id': 1, 'purchase_date': '2022-01-02'},
            ]
        },
        params={'country': 'UK'},
        run='result',
        order_by='purchase_date',
        expected=[
            {'name': 'John', 'product_name': 'Spell book', 'purchase_date': '2022-01-01', 'items': 2},
            {'name': 'John', 'product_name': 'Spell book', 'purchase_date': '2022-01-02', 'items': 1}
        ]
    )

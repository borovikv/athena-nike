import os.path

import pytest

from tests.specs_loader import spec_parameters, get_all_specs
from tests.sql import SpecExecutor
from toolbox.sql_utils import get_query

SPECS = get_all_specs('tests.specs')


@pytest.mark.parametrize(**spec_parameters(SPECS))
def test_spec(spec):
    execute = SpecExecutor(spec, port=8888)
    query_path = os.path.join(*list(filter(bool, [spec.get('path'), spec['scenario']])))
    sql = get_query(query_path)

    result = execute(sql, order_by=spec.get('order_by'), cte=spec['run'])

    expected = spec['expected']
    assert result == expected

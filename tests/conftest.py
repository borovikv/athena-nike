import os

import tests.specs_loader


def pytest_itemcollected(item):
    if os.getenv('FORMAT_NODE_ID') != 'TRUE':
        return
    if item._obj.__name__ == 'test_spec':
        item._nodeid = tests.specs_loader.build_nodeid(item._nodeid)
    else:
        item._nodeid += '\n' + item._obj.__doc__


def pytest_addoption(parser):
    parser.addoption("--run_name", action="store", default='all')


def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.run_name
    if 'run_name' in metafunc.fixturenames:
        metafunc.parametrize('run_name', [option_value])
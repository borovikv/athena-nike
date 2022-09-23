import tests.specs_loader


def pytest_itemcollected(item):
    if item._obj.__name__ == 'test_spec':
        item._nodeid = tests.specs_loader.build_nodeid(item._nodeid)

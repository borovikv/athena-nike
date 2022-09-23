import importlib
import os
import pkgutil
import re


def get_all_specs(specs_package):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    sql_specs = importlib.import_module(specs_package)
    path = os.path.join(base_dir, *specs_package.split('.'))
    modules = [name for _, name, _ in pkgutil.iter_modules([path])]
    specs = []
    for module in modules:
        importlib.import_module(f'{specs_package}.{module}')
        specs += getattr(getattr(sql_specs, module), 'SPECS')
    return specs


def spec_parameters(specs):
    return dict(argnames='spec', argvalues=specs, ids=[format_spec_name(spec) for spec in specs])


def format_spec_name(spec):
    name = 'execute "{run}" from {scenario}'.format(**spec)
    if 'description' in spec:
        return f'{name}#{spec["description"]}'
    elif 'when' in spec:
        return f'{name} when {spec["when"]}'
    return name


def build_nodeid(nodeid):
    match = re.match(r'(?P<file>[^:]+)::(?P<test_name>[^\[]+)\[(?P<spec>[^#]+)#(?P<docstring>[^]]+)]', nodeid)
    if match:
        parts = match.groupdict()
        docstring = '\n\t'.join(map(str.strip, parts['docstring'].split('\\n')))
        nodeid = f'{parts["file"]}::Spec: {parts["spec"]}\n{docstring}'
    return nodeid

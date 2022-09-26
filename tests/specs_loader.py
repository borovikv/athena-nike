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
        spec = getattr(getattr(sql_specs, module), 'SPECS')
        specs.append(spec)
    return specs


def spec_parameters(specs):
    ids = []
    argvalues = []
    for mod_spec in specs:
        for spec_name, spec in mod_spec.items():
            ids.append(format_spec_name(spec))
            argvalues.append((spec_name,spec))
    result = dict(argnames='spec_name,spec', argvalues=argvalues, ids=ids)
    return result


def format_spec_name(spec):
    name = 'execute "{run}" from {scenario}'.format(**spec)
    if 'description' in spec:
        return f'{name}#{spec["description"]}'
    elif 'when' in spec:
        return f'{name} when {spec["when"]}'
    return name


def build_nodeid(nodeid):
    pattern = r'(?P<file>[^:]+)::(?P<test_name>[^\[]+)\[([^-]+-){0,1}(?P<spec>[^#]+)#(?P<docstring>[^]]+)]'
    match = re.match(pattern, nodeid)
    if match:
        parts = match.groupdict()
        docstring = '\n\t'.join(map(str.strip, parts['docstring'].split('\\n')))
        nodeid = f'{parts["file"]}::Spec: {parts["spec"]}\n{docstring}'
    return nodeid

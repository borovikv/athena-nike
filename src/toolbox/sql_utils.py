import os

import jinja2


def get_query(path, **context):
    abs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
    with open(abs_path) as f:
        content = f.read()

    template = jinja2.Template(content)
    return template.render(**context)

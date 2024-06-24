import os
import types
import inspect
import importlib

from qiime2 import __version__

from sphinx.ext.linkcode import setup as linkcode_setup


if '+' in __version__:
    tag, local = __version__.split('+')
    q2ref = local.split('.')[1][1:]
elif 'dev' in __version__:
    q2ref = 'dev'
else:
    q2ref = __version__

URLS = {
    'qiime2': lambda rel, line: (
        f'https://github.com/qiime2/qiime2/tree/'
        f'{q2ref}/{rel}{f"#L{line + 1}" if line is not None else ""}'
    )
}


def find_object(module, path: list):
    while path and (component := path.pop(0)):
        element = getattr(module, component, None)
        if type(element) is types.ModuleType:
            module = element
        elif element is not None:
            break
    else:
        return None, None

    if path:
        component = path.pop(0)
        element = getattr(element, component, None)
        # we have a fake prefix, backtrack to the module
        if element is None:
            module, element = find_object(module, path)

    return module, element


def linkcode_resolve(domain, info):
    if domain != 'py':
        return None

    module_name = info['module']
    fullname = info['fullname']
    try:
        module = importlib.import_module(module_name)
    except Exception:
        return None

    root = module_name.split('.')[0]
    if root not in URLS:
        return None

    try:
        root_dir = os.path.join(
            os.path.dirname(importlib.import_module(root).__file__),
            '..'  # one more directory up from the base init
        )
    except Exception:
        return None

    path = fullname.split('.')
    module, element = find_object(module, path)
    if element is None:
        return None

    try:
        file = inspect.getsourcefile(element)
        assert file is not None
    except Exception:
        return None

    try:
        _, line = inspect.findsource(element)
    except Exception:
        line = None

    relpath = os.path.relpath(file, root_dir)

    return URLS[root](relpath, line)


def setup(app):
    app.config['linkcode_resolve'] = linkcode_resolve
    return linkcode_setup(app)

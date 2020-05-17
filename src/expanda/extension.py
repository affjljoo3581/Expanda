import importlib
from typing import Dict


class Extension(object):
    def __init__(self, module_name: str):
        # Import extension module.
        module = importlib.import_module(module_name)

        # Extension must contain `__extension__` variable in global.
        if not hasattr(module, '__extension__'):
            raise NotImplementedError(
                f'{module_name} is not an extension. This module does not have'
                f' `__extension__` variable.')
        ext = getattr(module, '__extension__')

        # Although other arguments can be replaced to default, `main` argument
        # which is actual extension implementation should be available.
        if 'main' not in ext:
            raise NotImplementedError(
                f'{module_name}.__extension__ should contain `main` key with'
                f' implementation.')

        self.module_name = module_name
        self.ext_name = ext.get('name', 'unknown')
        self.version = ext.get('version', '1.0.0')
        self.description = ext.get('description', '')
        self.author = ext.get('author', 'anonymous')
        self.main_func = ext.get('main')
        self.arg_reqs = ext.get('arguments', {})

    def call(self, input_file: str, output_file: str, temporary: str,
             raw_args: Dict[str, str]):
        args = {}
        for name, req in self.arg_reqs.items():
            if 'default' not in req and name not in raw_args:
                raise TypeError(f'missing required argument: `{name}`')

            # Cast the given arguments to required types.
            args[name] = req['type'](raw_args.get(name, req.get('default')))

        # Call extension main function with casted arguments.
        self.main_func(input_file, output_file, temporary, args)

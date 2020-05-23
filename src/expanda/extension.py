import importlib
from typing import Dict


class Extension(object):
    r"""Wrapper class of extension.

    Every extensions should define their informations into ``__extension__``
    variable. For using extensions, this wrapper class provides simple
    interface to handle them. It summarizes attributes and helps executing
    them.

    Caution:
        This class dynamically import the given `module_name`. Make sure that
        the extension module can be imported in current environment.

    Arguments:
        module_name (str): Module name of extension.
    """
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
        r"""Call main code of the extension.

        Note:
            Every extensions have their own parameter requirements in
            ``__extension__`` variable. This function automatically cast
            the type of each string-formatted raw argument.

        Arguments:
            input_file (str): Input file path.
            output_file (str): Output file path.
            temporary (str): Temporary directory where the extension would use.
            raw_args (dict): String-formatted raw arguments for extension.
        """
        args = {}
        for name, req in self.arg_reqs.items():
            if 'default' not in req and name not in raw_args:
                raise TypeError(f'missing required argument: `{name}`')

            # Cast the given arguments to required types.
            args[name] = req['type'](raw_args.get(name, req.get('default')))

        # Call extension main function with casted arguments.
        self.main_func(input_file, output_file, temporary, args)

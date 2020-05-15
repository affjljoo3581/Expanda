import re
import argparse
from configparser import ConfigParser
from .extension import Extension


def _show_extension_details(module_name):
    # Show the details of extension.
    ext = Extension(module_name)
    print(f'Extension [{ext.module_name}]\n'
          f'Name: {ext.ext_name}\n'
          f'Version: {ext.version}\n'
          f'Description: {ext.description}\n'
          f'Author: {ext.author}')


def _show_required_extension_list(config_file):
    # Read config file.
    config = ConfigParser()
    config.read(config_file)

    # Parse `input-files` option to get required extension list.
    input_files = config['DEFAULT'].get('input-files')
    exts = set(re.match(r'--(.*?)\s', line).groups()[0]
               for line in input_files.splitlines(False)
               if line)

    # Show the extension list tidily.
    print('{:25s}{:10s}'.format('Extension', 'Version'))
    print('=' * 35)
    for ext in exts:
        version = Extension(ext).version
        print(f'{ext[:25]:25s}{version[:10]:10s}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='expanda',
        description='Expanda - A universal integrated corpus generator')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # command line: expanda list [config]
    list_parser = subparsers.add_parser(
        'list', help='list required extensions in the workspace')
    list_parser.add_argument(
        'config', default='expanda.cfg', nargs='?',
        help='expanda configuration file')

    # command line: expanda show [extension]
    show_parser = subparsers.add_parser(
        'show', help='show extension information')
    show_parser.add_argument(
        'extension', help='module name of certain extension')

    # command line: expanda build [config]
    build_parser = subparsers.add_parser(
        'build', help='build dataset through given corpora')
    build_parser.add_argument(
        'config', default='expanda.cfg', nargs='?',
        help='expanda configuration file')

    args = parser.parse_args()
    if args.command == 'list':
        _show_required_extension_list(args.config)
    elif args.command == 'show':
        _show_extension_details(args.extension)
    elif args.command == 'build':
        pass

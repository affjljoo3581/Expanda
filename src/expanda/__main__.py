import re
import os
import shutil
import argparse
from configparser import ConfigParser
from .extension import Extension
from .shuffling import shuffle
from .tokenization import train_tokenizer, tokenize_corpus


def _show_extension_details(module_name: str):
    # Show the details of extension.
    ext = Extension(module_name)
    print(f'Extension [{ext.module_name}]\n'
          f'Name             : {ext.ext_name}\n'
          f'Version          : {ext.version}\n'
          f'Description      : {ext.description}\n'
          f'Author           : {ext.author}')

    # Print required parameters.
    print('Parameters')
    for name, opt in ext.arg_reqs.items():
        print('    {:12s} : {:6s}'.format(name, opt['type'].__name__), end='')
        if 'default' in opt:
            print(f' (default: {opt["default"]})')
        else:
            print('')


def _show_required_extension_list(config_file: str):
    # Read config file.
    config = ConfigParser()
    config.read(config_file)

    # Parse `input-files` option to get required extension list.
    input_files = config['DEFAULT'].get('input-files')
    exts = set(re.match(r'--(.*?)\s', line).group(0)
               for line in input_files.splitlines(False)
               if line)

    # Show the extension list tidily.
    print('{:25s}{:10s}'.format('Extension', 'Version'))
    print('=' * 35)
    for ext in exts:
        version = Extension(ext).version
        print(f'{ext[:25]:25s}{version[:10]:10s}')


def _build_corpus(config_file: str):
    # Read config file.
    config = ConfigParser()
    config.read(config_file)

    input_files = config['build'].get('input-files')
    input_files = [re.match(r'--(.*?)\s+(.*)', line.strip()).groups()
                   for line in input_files.splitlines(False)
                   if line]

    # Read arguments from configuration file.
    temporary = config['build'].get('temporary-path', './tmp')
    vocab = config['build'].get('output-vocab', 'vocab.txt')
    corpus = config['build'].get('output-corpus', 'corpus.txt')
    raw_corpus = config['build'].get('output-raw-corpus', 'corpus.raw.txt')

    subset_size = config['tokenize'].getint('subset-size', fallback=10000000)
    vocab_size = config['tokenize'].getint('vocab-size', fallback=8000)
    unk_token = config['tokenize'].get('unk-token', '<unk>')

    control_tokens = config['tokenize'].get('control-tokens', '')
    control_tokens = [token.strip()
                      for token in control_tokens.splitlines()
                      if token]

    # Create temporary directory if not exists.
    try:
        os.makedirs(temporary)
    except FileExistsError:
        pass

    # Extract raw corpus file to plain sentences.
    for ext, input_file in input_files:
        print(f'[*] execute extension [{ext}] for [{input_file}]')
        Extension(ext).call(input_file,
                            os.path.join(temporary, input_file),
                            temporary,
                            dict(config.items(ext)))

    # Gather the extracted plain text.
    print('[*] merge extracted texts...')
    with open(os.path.join(temporary, 'integrated'), 'wb') as dst:
        for _, input_file in input_files:
            with open(os.path.join(temporary, input_file), 'rb') as src:
                shutil.copyfileobj(src, dst)

    # Shuffle the text.
    print('[*] start shuffling merged corpus.')
    shuffle(os.path.join(temporary, 'integrated'), raw_corpus, temporary)

    # Train subword tokenizer and tokenize the corpus.
    train_tokenizer(raw_corpus, vocab, temporary, subset_size, vocab_size,
                    unk_token, control_tokens)
    tokenize_corpus(raw_corpus, corpus, vocab, unk_token, control_tokens)

    # Remove temporary directory.
    shutil.rmtree(temporary)

    print('[*] finish building corpus.')


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
        _build_corpus(args.config)

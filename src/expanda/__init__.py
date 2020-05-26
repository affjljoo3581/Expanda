import re
import os
import math
import shutil
import argparse
from configparser import ConfigParser
from .extension import Extension
from .shuffling import shuffle
from .tokenization import train_tokenizer, tokenize_corpus
from typing import List
from .utils import random_filename, random_filenames


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
    input_files = config['build'].get('input-files', fallback='')
    exts = set(re.match(r'--(.*?)\s', line).group(0)
               for line in input_files.splitlines(False)
               if line)

    # Show the extension list tidily.
    print('{:25s}{:10s}'.format('Extension', 'Version'))
    print('=' * 35)
    for ext in exts:
        version = Extension(ext).version
        print(f'{ext[:25]:25s}{version[:10]:10s}')


def _balancing_corpora(input_files: List[str], corpus_names: List[str],
                       temporary: str):
    corpus_size = [os.path.getsize(input_file)
                   for input_file in input_files]

    # Get maximum size and calculate repetition rate.
    max_size = max(corpus_size)
    expand_rate = [math.floor(max_size / size) for size in corpus_size]

    print('[*] balance the size for extracted texts.')
    for input_file, corpus_name, rate in zip(input_files,
                                             corpus_names,
                                             expand_rate):
        # Skip if no repetition case.
        if rate == 1:
            continue

        # Rename the origin file.
        print(f'[*] corpus [{corpus_name}] will be repeated {rate} times.')

        # Repeat the texts and save to the path of origin file.
        repeat_filename = random_filename(temporary)
        with open(input_file, 'rb') as src, \
                open(repeat_filename, 'wb') as dst:
            for _ in range(rate):
                src.seek(0)
                shutil.copyfileobj(src, dst)

        # Remove the origin file.
        os.remove(input_file)
        os.rename(repeat_filename, input_file)


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
    vocab = config['build'].get('output-vocab', 'build/vocab.txt')
    split_ratio = config['build'].getfloat('split-ratio', 0.1)

    train_corpus = config['build'].get('output-train-corpus',
                                       'build/corpus.train.txt')
    test_corpus = config['build'].get('output-test-corpus',
                                      'build/corpus.test.txt')
    raw_corpus = config['build'].get('output-raw-corpus',
                                     'build/corpus.raw.txt')

    subset_size = config['tokenization'].getint('subset-size',
                                                fallback=1000000000)
    vocab_size = config['tokenization'].getint('vocab-size', fallback=8000)
    limit_alphabet = config['tokenization'].getint('limit-alphabet',
                                                   fallback=1000)
    unk_token = config['tokenization'].get('unk-token', '<unk>')

    control_tokens = config['tokenization'].get('control-tokens', '')
    control_tokens = [token.strip()
                      for token in control_tokens.splitlines()
                      if token]

    # Create directories if not exists.
    def create_dir(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

    create_dir(os.path.dirname(vocab))
    create_dir(os.path.dirname(train_corpus))
    create_dir(os.path.dirname(test_corpus))
    create_dir(os.path.dirname(raw_corpus))
    create_dir(temporary)

    # Extract raw corpus file to plain sentences.
    extract_filenames = random_filenames(temporary, len(input_files))
    for (ext, input_file), name in zip(input_files, extract_filenames):
        print(f'[*] execute extension [{ext}] for [{input_file}]')
        Extension(ext).call(input_file,
                            name,
                            temporary,
                            dict(config.items(ext)))

    # Balance the size of each corpus.
    if config['build'].get('balancing', '').lower() == 'true':
        _balancing_corpora(extract_filenames,
                           [name for _, name in input_files],
                           temporary)

    # Gather the extracted plain text.
    print('[*] merge extracted texts.')
    integrate_filename = random_filename(temporary)
    with open(integrate_filename, 'wb') as dst:
        for name in extract_filenames:
            with open(name, 'rb') as src:
                shutil.copyfileobj(src, dst)
            os.remove(name)

    # Shuffle the text.
    print('[*] start shuffling merged corpus...')
    shuffle(integrate_filename, raw_corpus, temporary)
    os.remove(integrate_filename)

    # Train subword tokenizer and tokenize the corpus.
    print('[*] complete preparing corpus. start training tokenizer...')
    train_tokenizer(raw_corpus, vocab, temporary, subset_size, vocab_size,
                    limit_alphabet, unk_token, control_tokens)

    print('[*] create tokenized corpus.')
    tokenize_filename = random_filename(temporary)
    tokenize_corpus(raw_corpus, tokenize_filename, vocab, unk_token,
                    control_tokens)

    print('[*] split the corpus into train and test dataset.')
    with open(tokenize_filename, 'rb') as src:
        total_lines = 0
        for _ in src:
            total_lines += 1

        src.seek(0)

        # Write to test dataset.
        with open(test_corpus, 'wb') as dst:
            for i, line in enumerate(src):
                dst.write(line)
                if i >= total_lines * split_ratio:
                    break

        # Write to train dataset.
        with open(train_corpus, 'wb') as dst:
            shutil.copyfileobj(src, dst)
    os.remove(tokenize_filename)

    # Remove temporary directory.
    print('[*] remove temporary directory.')
    shutil.rmtree(temporary)

    print('[*] finish building corpus.')


def _main():
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

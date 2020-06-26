import os
import re
import kss
import ijson
import shutil
from typing import Dict, Any, Pattern
from multiprocessing import Process, Queue
from expanda.utils import random_filenames


def _create_pattern_dict() -> Dict[str, Pattern[str]]:
    return {'strokeout': re.compile(r'--.*?--|~~.*?~~'),
            'underline': re.compile(r'__(.*?)__'),
            'bold': re.compile(r'\'\'\'(.*?)\'\'\''),
            'italics': re.compile(r'\'\'(.*?)\'\''),
            'link': re.compile(r'\[\[(?:[^]]*?\|)?(.*?)(?:#.*?)?\]\]'),
            'macro': re.compile(r'\[.*?\]'),
            'bracket': re.compile(r'\([^(]*?\)'),
            'others': re.compile(r'^[ >*|].*?', re.M),
            'single-quote': re.compile('[\x60\xb4\u2018\u2019]'),
            'double-quote': re.compile('[\u201c\u201d]')}


def _modified_removing_lines_without_punctuation(text: str) -> str:
    filtered = []
    for line in text.splitlines():
        line = line.rstrip()
        if line and line[-1] in '.!?':
            filtered.append(line)
    return '\n'.join(filtered)


def _modified_removing_unnecessary_spaces(text: str) -> str:
    replaced = text.replace('\n', ' ').replace('\t', ' ')
    while '  ' in replaced:
        replaced = replaced.replace('  ', ' ')
    return replaced


def _clean_wiki_text(code: str, patterns: Dict[str, Pattern[str]]) -> str:
    # Remove strokeouts and clear underlines.
    code = patterns['strokeout'].sub('', code)
    code = patterns['underline'].sub(r'\1', code)

    # Clear bold and italics text.
    while patterns['bold'].search(code):
        code = patterns['bold'].sub(r'\1', code)

    while patterns['italics'].search(code):
        code = patterns['italics'].sub(r'\1', code)

    # Render links and macros.
    code = patterns['link'].sub(r'\1', code)
    code = patterns['macro'].sub('', code)

    # Cleanup the rest messy texts.

    # Instead of using below comment code, using modified function consumes
    # much faster.
    # code = patterns['without_punct'].sub('', code)
    code = _modified_removing_lines_without_punctuation(code)

    code = patterns['others'].sub('', code)

    # Instead of using below comment code, using modified function consumes
    # much faster.
    # while patterns['spacing'].search(code):
    #     code = patterns['spacing'].sub(' ', code)
    code = _modified_removing_unnecessary_spaces(code)

    # Remove unnecessary brackets.
    while patterns['bracket'].search(code):
        code = patterns['bracket'].sub('', code)

    # Replace unusual quotes.
    code = patterns['single-quote'].sub('\'', code)
    code = patterns['double-quote'].sub('"', code)

    return code


def _process_article_worker(output_file: str, queue: Queue):
    with open(output_file, 'w', encoding='utf-8') as fp:
        patterns = _create_pattern_dict()
        while True:
            code = queue.get()
            if code is None:
                break

            # Write cleaned wiki articles into the output file.
            fp.write(_clean_wiki_text(code, patterns) + '\n\n')


def _tokenize_sentences_worker(input_file: str, output_file: str,
                               min_len: int, max_len: int,
                               split_sent: bool = True):
    with open(input_file, 'r', encoding='utf-8') as src, \
            open(output_file, 'w', encoding='utf-8') as dst:
        total_lines = ''
        for line in src:
            if not line.strip():
                if not split_sent and len(total_lines.strip()) > min_len:
                    dst.write(total_lines.strip() + '\n')
                continue

            for s in kss.split_sentences(line):
                # Skip extraordinary sentences
                s = s.strip()
                if s and s[0] in '*<-|':
                    continue

                if split_sent:
                    if len(s) > min_len and len(s.strip()) < max_len:
                        dst.write(s + '\n')
                else:
                    if len(total_lines) + len(s) > max_len:
                        dst.write(total_lines.strip() + '\n')
                        total_lines = ''
                    total_lines += s + ' '


def _extract_namu_wiki_json(input_file: str, output_file: str, temporary: str,
                            args: Dict[str, Any]):
    # Prepare processes and queue for serving extracted wiki articles.
    workers = []
    queue = Queue(maxsize=50 * args['num-cores'])
    extract_filenames = random_filenames(temporary, args['num-cores'])

    for i in range(args['num-cores']):
        w = Process(target=_process_article_worker,
                    args=(extract_filenames[i], queue))
        w.daemon = True
        w.start()
        workers.append(w)

    # Open `input_file` wiki dump and parse json data.
    with open(input_file, 'r', encoding='utf-8') as fp:
        parser = ijson.parse(fp)

        for prefix, event, value in parser:
            if not prefix.endswith('.text'):
                continue

            # Skip redirection pages.
            if value.lower().strip().startswith('#redirect'):
                continue

            # Serve raw-formatted wiki article to the processes.
            queue.put(value)

    # Notify the processes of that parsing is finished and wait for terminating
    # the processes.
    for _ in range(args['num-cores']):
        queue.put(None)
    for w in workers:
        w.join()

    # Start tokenization processes.
    workers = []
    split_filenames = random_filenames(temporary, args['num-cores'])

    for i in range(args['num-cores']):
        w = Process(target=_tokenize_sentences_worker,
                    args=(extract_filenames[i],
                          split_filenames[i],
                          args['min-length'],
                          args['max-length'],
                          args['split-sent'] == 'true'))
        w.daemon = True
        w.start()

        workers.append(w)

    # Wait for terminating the processes and remove temporarily created files.
    for w in workers:
        w.join()
    for name in extract_filenames:
        os.remove(name)

    # Merge all tokenized files into `output_file`.
    with open(output_file, 'wb') as dst:
        for name in split_filenames:
            with open(name, 'rb') as src:
                shutil.copyfileobj(src, dst)

    # Remove temporary files.
    for name in split_filenames:
        os.remove(name)


__extension__ = {
    'name': 'namuwiki extractor',
    'version': '1.0',
    'description': 'extract namuwiki json file.',
    'author': 'expanda',
    'main': _extract_namu_wiki_json,
    'arguments': {
        'num-cores': {'type': int, 'default': 1},
        'min-length': {'type': int, 'default': 50},
        'max-length': {'type': int, 'default': 1000},
        'split-sent': {'type': str, 'default': 'true'},
    }
}

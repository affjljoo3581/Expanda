import os
import re
import kss
import ijson
import shutil
from typing import Dict, Any
from multiprocessing import Process, Queue


def _create_pattern_dict() -> Dict[str, re.Pattern]:
    return {'without_punct': re.compile(r'.*[^.!?\s]\s*$', re.M),
            'strokeout': re.compile(r'--.*?--|~~.*?~~'),
            'underline': re.compile(r'__(.*?)__'),
            'bold': re.compile(r'\'\'\'(.*?)\'\'\''),
            'italics': re.compile(r'\'\'(.*?)\'\''),
            'link': re.compile(r'\[\[([^]]*?\|)?(?P<name>.*?)(#.*?)?\]\]'),
            'macro': re.compile(r'\[.*?\]'),
            'others': re.compile(r'^[ >].*?', re.M),
            'spacing': re.compile(r'\s{2}')}


def _clean_wiki_text(code: str, patterns: Dict[str, re.Pattern]) -> str:
    # Remove strokeouts and clear underlines.
    code = patterns['strokeout'].sub('', code)
    code = patterns['underline'].sub(r'\1', code)

    # Clear bold and italics text.
    while patterns['bold'].search(code):
        code = patterns['bold'].sub(r'\1', code)

    while patterns['italics'].search(code):
        code = patterns['italics'].sub(r'\1', code)

    # Render links and macros.
    code = patterns['link'].sub(r'\g<name>', code)
    code = patterns['macro'].sub('', code)

    # Cleanup the rest messy texts.
    code = patterns['without_punct'].sub('', code)
    code = patterns['others'].sub('', code)

    while patterns['spacing'].search(code):
        code = patterns['spacing'].sub(' ', code)

    return code


def _process_article_worker(output_file: str, queue: Queue):
    file = open(output_file, 'w', encoding='utf-8')

    patterns = _create_pattern_dict()
    while True:
        code = queue.get()
        if code is None:
            break

        # Write cleaned wiki articles into the output file.
        file.write(_clean_wiki_text(code, patterns) + '\n')

    file.close()


def _tokenize_sentences_worker(input_file: str, output_file: str,
                               min_len: int):
    with open(input_file, 'r', encoding='utf-8') as src, \
            open(output_file, 'w', encoding='utf-8') as dst:
        for line in src:
            for s in kss.split_sentences(line):
                if len(s.strip()) < min_len:
                    continue

                dst.write(s.strip() + '\n')


def _extract_namu_wiki_json(input_file: str, output_file: str, temporary: str,
                            args: Dict[str, Any]):
    # Prepare processes and queue for serving extracted wiki articles.
    workers = []
    queue = Queue(maxsize=10 * args['num-cores'])

    for i in range(args['num-cores']):
        w = Process(target=_process_article_worker,
                    args=(os.path.join(temporary, f'wiki{i}'), queue))
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
    for i in range(args['num-cores']):
        w = Process(target=_tokenize_sentences_worker,
                    args=(os.path.join(temporary, f'wiki{i}'),
                          os.path.join(temporary, f'split{i}'),
                          args['min-length']))
        w.daemon = True
        w.start()

        workers.append(w)

    # Wait for terminating the processes and remove temporarily created files.
    for w in workers:
        w.join()
    for i in range(args['num-cores']):
        os.remove(os.path.join(temporary, f'wiki{i}'))

    # Merge all tokenized files into `output_file`.
    with open(output_file, 'wb') as dst:
        for i in range(args['num-cores']):
            with open(os.path.join(temporary, f'split{i}'), 'rb') as src:
                shutil.copyfileobj(src, dst)

    # Remove temporary files.
    #for i in range(args['num-cores']):
    #    os.remove(os.path.join(temporary, f'split{i}'))


__extension__ = {
    'name': 'namuwiki extractor',
    'version': '1.0',
    'description': 'extract namuwiki json file.',
    'author': 'expanda',
    'main': _extract_namu_wiki_json,
    'arguments': {
        'num-cores': {'type': int, 'default': 1},
        'min-length': {'type': int, 'default': 50}
    }
}



def _extract_wiki_corpus(input_files, output_file, temporary, args):
    pass


__extension__ = {
    'name': 'wikipedia dump extractor',
    'version': '1.0',
    'description': 'extract wiki dump file.',
    'author': 'expanda',
    'main': _extract_wiki_corpus,
    'arguments': {
        'num-cores': {'type': int, 'default': 4}
    }
}

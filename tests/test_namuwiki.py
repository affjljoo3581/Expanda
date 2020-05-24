from expanda.ext import namuwiki
from expanda.utils import random_filename
import tempfile


def test_extracting_wiki_text_well():
    # Read NamuMark-format wiki code.
    with open('tests/res/namuwiki.raw.txt', 'r') as fp:
        wiki_code = fp.read()

    # Check if the code is precisely cleaned.
    with open('tests/res/namuwiki.plain.txt', 'r') as fp:
        patterns = namuwiki._create_pattern_dict()
        assert namuwiki._clean_wiki_text(wiki_code, patterns) == fp.read()


def test_splitting_sentences():
    # Use temporary directory since mocking is hard to apply to
    # `_tokenize_sentences_worker`.
    input_file = random_filename(tempfile.gettempdir())
    output_file = random_filename(tempfile.gettempdir())

    # Write dummy file to `input_file`.
    dummy = '안녕하세요. 반갑습니다! 어떠신가요? 괜찮습니다...ㅎㅎ'
    with open(input_file, 'w') as fp:
        fp.write(dummy)

    # Split the sentences.
    namuwiki._tokenize_sentences_worker(
        input_file, output_file, min_len=0)

    # Check if sentences are splitted well.
    with open(output_file, 'r') as fp:
        lines = fp.readlines()
        assert len(lines) == 4
        assert ' '.join([line.strip() for line in lines]) == dummy

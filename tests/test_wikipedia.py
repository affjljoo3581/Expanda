from expanda.ext import wikipedia
from expanda.utils import random_filename
import tempfile


def test_extracting_wiki_text_well():
    # Read MediaWiki-format wiki code.
    with open('tests/res/wikipedia.raw.txt', 'r') as fp:
        wiki_code = fp.read()

    # Check if the code is precisely cleaned.
    with open('tests/res/wikipedia.plain.txt', 'r') as fp:
        assert wikipedia._clean_wiki_text(wiki_code) == fp.read()


def test_splitting_sentences():
    # Use temporary directory since mocking is hard to apply to
    # `_tokenize_sentences_worker`.
    input_file = random_filename(tempfile.gettempdir())
    output_file = random_filename(tempfile.gettempdir())

    # Write dummy file to `input_file`.
    dummy = 'Nice to meet you Dr. John. Welcome! How are you?'
    with open(input_file, 'w') as fp:
        fp.write(dummy)

    # Split the sentences.
    wikipedia._prepare_tokenizing_sentences('en')
    wikipedia._tokenize_sentences_worker(input_file, output_file, 'en', 0, 100)

    # Check if sentences are splitted well.
    with open(output_file, 'r') as fp:
        lines = fp.readlines()
        assert len(lines) == 3
        assert ' '.join([line.strip() for line in lines]) == dummy

    # Check if splitting into chuncks works well.
    wikipedia._tokenize_sentences_worker(
        input_file, output_file, 'en', 0, 100, split_sent=False)

    with open(output_file, 'r') as fp:
        lines = fp.readlines()
        assert len(lines) == 1
        assert lines[0].strip() == dummy

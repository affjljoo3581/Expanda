from expanda.tokenization import train_tokenizer, tokenize_corpus
from expanda.utils import random_filename
import tempfile
import shutil
import os


def test_training_tokenizer_well():
    # Use temporary directory since `tokenizers` does not support mocking.
    input_file = random_filename(tempfile.gettempdir())
    vocab_file = random_filename(tempfile.gettempdir())

    # Copy dummy corpus file to `input_file`.
    shutil.copyfile('tests/res/wikipedia.plain.txt', input_file)

    # Train tokenizer with dummy corpus file.
    train_tokenizer(input_file,
                    vocab_file,
                    tempfile.gettempdir(),
                    vocab_size=100)

    # Check that the tokenizer is trained well.
    with open(vocab_file, 'r') as fp:
        assert len(fp.readlines()) == 100

    # Remove created temporary files.
    os.remove(input_file)
    os.remove(vocab_file)


def test_tokenizing_corpus_well():
    # Use temporary directory since `tokenizers` does not support mocking.
    input_file = random_filename(tempfile.gettempdir())
    vocab_file = random_filename(tempfile.gettempdir())
    output_file = random_filename(tempfile.gettempdir())

    # Copy dummy corpus file to `input_file`.
    shutil.copyfile('tests/res/wikipedia.plain.txt', input_file)

    # First of all, train the tokenizer to tokenize corpus.
    train_tokenizer(input_file,
                    vocab_file,
                    tempfile.gettempdir(),
                    vocab_size=100)

    # Next, tokenize the given corpus by using trained tokenizer.
    tokenize_corpus(input_file, output_file, vocab_file)

    # Check the corpus is tokenized well.
    with open(output_file, 'r') as output, \
            open('tests/res/wikipedia.plain.txt', 'r') as dummy:
        assert (output.read().strip().count('\n')
                == dummy.read().strip().count('\n'))

    # Remove created temporary files.
    os.remove(vocab_file)
    os.remove(input_file)

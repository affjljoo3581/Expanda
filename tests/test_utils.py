from expanda.utils import BufferedFileWriter, BufferedFileReader
from unittest import mock
from io import StringIO
import random
import string
import math


def _sample_exp_dist(lam):
    return math.floor(-math.log(random.random() + 1e-7) / lam)


def _generate_dummy_data():
    # Sample unicode subset.
    unicode_sets = [chr(i) for i in range(ord('가'), ord('힣'))]
    random.shuffle(unicode_sets)
    unicode_sets = ''.join(unicode_sets[:len(string.ascii_letters)])

    # Create random letter candidates.
    letters = (string.ascii_letters
               + string.punctuation
               + string.digits
               + unicode_sets
               + ' \t')

    # Generate 30 randomly sampled sentences.
    return '\n'.join([
        ''.join(random.choices(letters, k=_sample_exp_dist(1 / 30)))
        for _ in range(30)])


@mock.patch('builtins.open')
def test_buffered_file_reader(mock_open):
    # Create dummy data and mock builtin `open` function.
    data = _generate_dummy_data()
    mock_open.return_value = StringIO(data)

    reader = BufferedFileReader('', buffer_size=10)

    # Read lines from dummy file through the reader.
    lines = []
    while True:
        line = reader.readline()
        if not line:
            break
        lines.append(line)

    assert lines == data.splitlines(keepends=True)
    reader.close()


@mock.patch('builtins.open')
def test_buffered_file_writer(mock_open):
    # Create dummy buffer and mock builtin `open` function.
    buffer = StringIO()
    mock_open.return_value = buffer

    writer = BufferedFileWriter('', buffer_size=10)

    # Write lines to dummy file through the writer.
    data = _generate_dummy_data()
    for line in data.splitlines(keepends=True):
        writer.write(line)
    writer.flush()

    assert buffer.getvalue() == data
    writer.close()

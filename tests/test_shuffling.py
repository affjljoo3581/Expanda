from expanda.shuffling import shuffle
from unittest import mock
from io import BytesIO


class _modified_open_wrapper(object):
    def __init__(self):
        self.file_table = {}

    def __call__(self, path, mode):
        # Return already created fake file.
        if path in self.file_table:
            return self.file_table[path]

        # Modify `close` method to prevent actually close the buffer.
        def modified_close():
            self.file_table[path].seek(0)

        # Create fake file using 'BytesIO' which is similary to file.
        self.file_table[path] = BytesIO()
        self.file_table[path].close = modified_close
        return self.file_table[path]


@mock.patch('os.remove')
@mock.patch('builtins.open')
def test_shuffling_integrity(mock_open, mock_remove):
    mock_open.side_effect = _modified_open_wrapper()

    # Create target file.
    original = list(range(100))
    with open('input', 'wb') as fp:
        fp.write(b'\n'.join([str(i).encode() for i in original]))

    # Shuffle the file and write to `output`.
    shuffle('input', 'output', 'tmp')

    # Read shuffled file.
    with open('output', 'rb') as fp:
        shuffled = [int(i.decode()) for i in fp.readlines()]

    assert sorted(shuffled) == original

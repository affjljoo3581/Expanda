import os
import random
import string
from typing import List


_CANDIDATES = string.digits + string.ascii_lowercase


def random_filename(parent: str) -> str:
    r"""Generate random filename consists of 16 characters.

    Arguments:
        parent (str): Parent directory for file.

    Returns:
        Randomly generated file name.
    """
    return os.path.join(parent, ''.join(random.choices(_CANDIDATES, k=16)))


def random_filenames(parent: str, n: int) -> List[str]:
    r"""Generate multiple random filenames.

    Arguments:
        parent (str): Parent directory for files.
        n (int): Total number of filenames.

    Returns:
        Randomly generated file names.
    """
    return [random_filename(parent) for _ in range(n)]

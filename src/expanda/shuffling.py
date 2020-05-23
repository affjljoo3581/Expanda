import os
import tqdm
import random
import shutil
import argparse
from typing import List, IO
from .utils import random_filenames


_BEST_SEEK_CNT = 100000
_MAX_BUCKETS = 512


def _get_file_lines(fp: IO[bytes]) -> int:
    fp.seek(0)

    num_lines = 0
    for line in fp:
        num_lines += 1

    return num_lines


def _list_seek_offsets(fp: IO[bytes], stride: int = 1) -> List[int]:
    fp.seek(0)

    offsets = []
    while True:
        offsets.append(fp.tell())

        # Read `stride` lines and move after the lines.
        lines = [fp.readline() for _ in range(stride)]
        if not lines[-1]:
            break

    return offsets


def shuffle(input_file: str, output_file: str, temporary: str):
    r"""Shuffle text file with temporary buckets.

    Caution:
        Instead of allocating memory directly, this shuffling algorithm uses
        temporary bucket files which are in `temporary` directory. Please be
        careful not to delete the temporary files while executing this
        function.

    Arguments:
        input_file (str): Input file path.
        output_file (str): Output file path.
        temporary (str): Temporary directory where the buckets would be saved.
    """
    src = open(input_file, 'rb')

    # Calculate optimimum number of strides and buckets.
    stride = max(1, _get_file_lines(src) // _BEST_SEEK_CNT)
    buckets = min(stride * 2, _MAX_BUCKETS)
    print(f'[*] optimum stride: {stride}, buckets: {buckets}')

    # Create temporary bucket files.
    print('[*] create temporary bucket files.')
    bucket_filenames = random_filenames(temporary, buckets)
    dsts = [open(name, 'wb') for name in bucket_filenames]

    # Get offsets from input file.
    offsets = _list_seek_offsets(src, stride)
    random.shuffle(offsets)
    print(f'[*] successfully shuffle offsets. total offsets: {len(offsets)}')

    for off in tqdm.tqdm(offsets, desc='[*] shuffle input file'):
        # Move to the random offset.
        src.seek(off)

        for _ in range(stride):
            line = src.readline()
            if not line:
                break

            if not line.endswith(b'\n'):
                line = line + b'\n'

            # Write the line to random bucket.
            dsts[random.randint(0, buckets - 1)].write(line)

    # Close all resources.
    src.close()
    for d in dsts:
        d.close()

    # Copy shuffled separations to the output file.
    print('[*] start copying buckets to the output file.')
    with open(output_file, 'wb') as dst:
        for name in bucket_filenames:
            with open(name, 'rb') as src:
                shutil.copyfileobj(src, dst)
    print('[*] finish copying buckets. remove the buckets...')

    # Remove the temporary bucket files.
    for name in bucket_filenames:
        os.remove(name)


def _main():
    parser = argparse.ArgumentParser(
        prog='expanda-shuffling',
        description='approximately shuffle text file.')
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--tmp', default='tmp',
                        help='temporary directory path')
    args = parser.parse_args()

    # Create temporary directory if not exists.
    remove_after_shuffling = False
    if not os.path.exists(args.tmp):
        os.makedirs(args.tmp)
        remove_after_shuffling = True

    # Shuffle the text file.
    shuffle(args.input, args.output, args.tmp)

    # Remove created temporary directory.
    if remove_after_shuffling:
        os.removedirs(args.tmp)


if __name__ == '__main__':
    _main()

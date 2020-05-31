expanda.shuffling
=================
.. currentmodule:: expanda.shuffling

Introduction
~~~~~~~~~~~~
Common shuffling algorithms ensure almost perfect randomness and are efficient
(usually have :math:`O(n)` complexity). However, they consume a lot of memories
while shuffling large files. For instance, using shuf_ to shuffle 5GB of file
may occur memory error in small system. In most cases, the whole data would be
copied to the memory. Besides, some algorithms require several times more than
memory.

Let's consider the case of solving NLP problems in deep learning. Because a
larger corpus leads to better performance, many texts should be gathered into
the corpus. GPT-2 was trained with **40GB** text ([#]_) and RoBERTa was so with
**160GB** text ([#]_). In fact, shuffling whole data in the memory is
impossible. Due to the large file size, other memory-efficient methods are
needed.

The simplest way to solve the problem is in **seeking**. First, collect the
starting position of each line. It is as follows:

.. code-block:: python

    offsets = [src.tell()]

    line = src.readline()
    while line:
        offsets.append(src.tell())
        line = src.readline()

After collecting the positions, simply shuffle them. Seeking to each offset and
copying lines will provide complete shuffling. It is as described below:

.. code-block:: python

    random.shuffle(offsets)
    for off in offsets:
        src.seek(off)
        dst.write(src.readline())

However, this algorithm empirically takes minutes to shuffle a mere 500MB text
which consists of 10M sentences while shuf_ takes about 5 seconds. Though less
memory usage is an obvious advantage, extremely slow speed is fatal.

Theoretically, complexity of *seeking* is :math:`O(1)`. Then, why the above
codes are enormously inefficient? That is probably related to python's I/O
implementation. First, **python is too slow to handle large files in detail**.
Python implementation of shuf_ is about 3 times slower than the original. To
reduce I/O bottlenecks, python provides *buffering* in file. However, if the
position of file is moved to random offset, then the buffered data will become
useless. Consequently, you cannot use *buffering* when using *seeking*
frequently.

Hence, we decided to approximate shuffling. We empirically found optimum
seeking counts. In our experiments, seeking **10M** times is not critical for
performance. According to the result, we propose a revised algorithm to shuffle
large files efficiently. *Seeking file* would be called up to **10M** times.
Each seeks position indicates a start of chunk. The chunks would be shuffled
locally and randomly distributed to buckets. Basically, twice as many buckets
as chunks are needed. After splitting the file randomly, the buckets will be
merged into one.

We have observed that the approximation ensures almost perfect randomness and
seems sufficient in natural language. We tested the algorithm with 5GB of file
and it takes about 3 minutes without any memory errors.

You can run this module alone for shuffling. See `Command-line Usage`_.

Functions
~~~~~~~~~
.. autofunction:: shuffle

Command-line Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: console

    usage: expanda-shuffling [-h] [--tmp TMP] input output

    approximately shuffle text file.

    positional arguments:
      input
      output

    optional arguments:
      -h, --help  show this help message and exit
      --tmp TMP   temporary directory path


References
~~~~~~~~~~
.. [#] https://openai.com/blog/better-language-models/
.. [#] Y\. Liu, M. Ott et al. 2019. "RoBERTa: A Robustly Optimized BERT Pretraining Approach"
.. _shuf: https://www.gnu.org/software/coreutils/manual/html_node/shuf-invocation.html

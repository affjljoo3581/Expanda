.. _`expanda.extension`:

expanda.extension
=================
.. currentmodule:: expanda.extension

Introduction
------------
Corpora, which are crawled or downloaded from Internet, have diverse
structures and formats. That is because **the purpose of each content is
different**. For instance, *Wikipedia* is a collection of articles and
*Twitter* consists of tweets. Futhermore, **structures are even changed by
platforms of corpus contents**. Same wiki contents can have different
structures depending on their wiki engines.

The very purpose of *expanda* is to integrate procedures and pipelines for
building corpus dataset. In order to consolidate the process with various
corpora, their formats should be regularized equally.

This module, for that reasons, provides an interface to construct
regularization procedures for corresponding corpus formats. The regularization
procedures are treated as **extensions** and literally, everyone can write
codes for parsing their own corpus.

Every extensions should have ``__extension__`` variable in global. Basic form
of the variable is as follows:

.. code:: python

    __extension__ = {
        'name': 'The name of extension',
        'version': '1.0',
        'description': 'This is a simple example of extension',
        'author': 'Who write this code?',
        'main': <extension implementation>,
        'arguments': {
            'param name': {'type': <param type>, 'default': <default>},
            ...
        }
    }

Expanda uses extension by importing corresponding module, so ``__extension__``
variable must be in global scope of the module. All informations except `main`
are optional. There is no problem to skip writting the informations. But `main`
parameter, which is an implementation of the extension, should be defined in
``__extension__`` variable. The implementation function would get 4 arguments:

.. code:: python

    def main_code(input_file: str, output_file: str, temporary: str, args: Dict[str, Any]):
        # Implementation of the extension...

`input_file` and `output_file` are literally an input raw-format corpus file
and parsed output file respectively. `temporary` is an assigned temporary
directory to use while executing the extension. `args` is a dictionary from
**expanda configuration**. Note that arguments would be casted to the types
defined in ``__extension__``.

The role of implementation is simple. Read the given `input_file` and extract
to plain text. After splitting the text into single sentences, save the
sentences to `output_file`. Expanda will summarize pipelines from configuration
and automatically execute extensions. Extracted texts are combined and other
procedures are applied to the corpora.

Expanda provides some useful extensions in ``expanda.ext`` package. See also
:ref:`extensions`.

.. note::
    While extracting corpus, `temporary files` might be needed. Expanda
    recommends to use :ref:`utils for extension` when creating
    `temporary files`. All extensions Expanda provides create files with
    ``random_filename`` and ``random_filenames``.

Classes
-------
.. autoclass:: Extension
    :members:

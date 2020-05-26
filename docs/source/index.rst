.. Expanda documentation master file, created by
   sphinx-quickstart on Wed May 13 21:22:32 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Expanda documentation
=====================

Introduction
------------
**Expanda** is an **integrated corpus-building environment**. Expanda provides
integrated pipelines for building corpus dataset. Building corpus dataset
requires several complicated pipelines such as parsing, shuffling and
tokenization. If the corpora are gathered from different applications, it would
be a problem to parse various formats. Expanda helps to build corpus simply at
once by setting build configuration.

Dependencies
------------
* nltk
* ijson
* tqdm>=4.46.0
* mwparserfromhell>=0.5.4
* tokenizers>=0.7.0
* kss==1.3.1

Installation
------------


With pip
^^^^^^^^
Expanda can be installed using pip as follows:

.. code:: console

   $ pip install expanda


From source
^^^^^^^^^^^
You can install from source by cloning the repository and running:

.. code:: console

   $ git clone https://github.com/affjljoo3581/Expanda.git
   $ cd Expanda
   $ python setup.py install


Command-line Usage
------------------
You can use the features of Expanda in command-line.

Build Dataset
^^^^^^^^^^^^^
``expanda build`` command builds corpus dataset through the given build
configuration file. Detail is as follows:

.. code:: console

   usage: expanda build [-h] [config]

   positional arguments:
     config      expanda configuration file

   optional arguments:
     -h, --help  show this help message and exit

Show Extension Detail
^^^^^^^^^^^^^^^^^^^^^
After installing extensions, you can check if the extensions are recognizable.
Expanda loads extensions by importing corresponding modules. If certain
extensions are installed in **different virtual environment**, Expanda cannot
use the extensions. So before building the dataset, check whether the
extensions are accessible or not. ``expanda show`` command shows the details of
the given extension. Detail is as follows:

.. code:: console

   usage: expanda show [-h] extension

   positional arguments:
     extension   module name of certain extension

   optional arguments:
     -h, --help  show this help message and exit

List of Required Extensions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
``expanda list`` command shows a list of extensions defined in the given
configuration. Namely, you can see which extensions are used in this dataset.
Detail is as follows:

.. code:: console

   usage: expanda list [-h] [config]

   positional arguments:
     config      expanda configuration file

   optional arguments:
     -h, --help  show this help message and exit

Build Configuration
-------------------
Before building corpus, you need to setup *build configuration* in workspace
first. The configuration file follows **INI format**. Here is an example:

.. code:: ini

   # extension configurations
   # ...

   [tokenization]
   subset-size         = 1000000000
   vocab-size          = 32000
   limit-alphabet      = 6000

   unk-token           = <unk>
   control-tokens      = <s>
                         </s>
                         <pad>

   [build]
   input-files         =
       --my.extension.foo1    src/bar1.xml
       --my.extension.foo2    src/bar2.txt
       --my.extension.foo3    src/bar3.xml.bz2
   balancing           = true
   split-ratio         = 0.1

   temporary-path      = tmp

   output-vocab        = build/vocab.txt
   output-train-corpus = build/corpus.train.txt
   output-test-corpus  = build/corpus.test.txt
   output-raw-corpus   = build/corpus.raw.txt

Basically, you need to configure two sections -- **tokenization** and
**build**. **tokenization** section contains arguments for tokenizing texts,
described in :ref:`tokenization`. You can declare symbol names and define
tokenization options. In **build** section, you can set input, output files and
temporary directory. ``balancing`` determines whether to modify the amount of
each corpus uniformly. 

Perhaps extensions used for constructing the dataset would need their own
options in extracting. You can configure the options in each section with the
corresponding module name. See also :ref:`expanda.extension`.

After building the dataset, the workspace should be as below:

.. code::

   workspace
   ├── build
   │     ├── corpus.raw.txt
   │     ├── corpus.train.txt
   │     ├── corpus.test.txt
   │     └── vocab.txt
   ├── src
   │     ├── bar1.xml
   │     ├── bar2.txt
   │     └── bar3.xml.bz2
   └── expanda.cfg


Modules
-------
Expanda contains pipeline modules for building corpus dataset. Some useful
modules can be used in command-line independently.

.. toctree::
   :maxdepth: 1

   expanda.shuffling
   expanda.tokenization
   expanda.extension
   expanda.utils

.. _`extensions`:

Extensions
----------
Expanda provides basic extensions to help parsing corpus file. You can use the
extensions without any additional installations.

.. toctree::
   :maxdepth: 1

   expanda.ext.wikipedia
   expanda.ext.namuwiki


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

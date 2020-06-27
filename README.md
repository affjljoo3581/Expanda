# Expanda

**The universal integrated corpus-building environment.**

[![PyPI version](https://badge.fury.io/py/Expanda.svg)](https://badge.fury.io/py/Expanda)
![build](https://github.com/affjljoo3581/Expanda/workflows/build/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/expanda/badge/?version=latest)](https://expanda.readthedocs.io/en/latest/?badge=latest)
![GitHub](https://img.shields.io/github/license/affjljoo3581/Expanda)
[![codecov](https://codecov.io/gh/affjljoo3581/Expanda/branch/master/graph/badge.svg)](https://codecov.io/gh/affjljoo3581/Expanda)
[![CodeFactor](https://www.codefactor.io/repository/github/affjljoo3581/expanda/badge)](https://www.codefactor.io/repository/github/affjljoo3581/expanda)

## Introduction
**Expanda** is an **integrated corpus-building environment**. Expanda provides
integrated pipelines for building a corpus dataset. Building corpus dataset
requires several complicated pipelines such as parsing, shuffling, and
tokenization. If the corpora are gathered from different applications, it would
be a problem to parse various formats. Expanda helps to build corpus simply at
once by setting build configuration.

For more information, see also [documentation](https://expanda.readthedocs.io/en/latest/).

## Main Features
* Easy to build, simple for adding new extensions
* Manages build environment systemically
* Fast build through performance optimization (even written in Python)
* Supports multi-processing
* Extremely less memory usage
* Don't need to write new codes for each corpus. Just write one line for adding
  a new corpus.

## Dependencies
* nltk
* ijson
* tqdm>=4.46.0
* mwparserfromhell>=0.5.4
* tokenizers>=0.7.0
* kss==1.3.1

## Installation

### With pip
Expanda can be installed using pip as follows:

```console
$ pip install expanda
```

### From source
You can install from source by cloning the repository and running:

```console
$ git clone https://github.com/affjljoo3581/Expanda.git
$ cd Expanda
$ python setup.py install
```

## Build your first dataset
Let's build **Wikipedia** dataset by using Expanda. First of all, install
Expanda.
```console
$ pip install expanda
```
Next, create a workspace to build dataset by running:
```console
$ mkdir workspace
$ cd workspace
```
Then, download Wikipedia dump file from [here](https://dumps.wikimedia.org/).
In this example, we are going to test with [part of the wiki](https://dumps.wikimedia.org/enwiki/20200520/enwiki-20200520-pages-articles1.xml-p1p30303.bz2).
Download the file through the browser, move to `workspace/src` and rename to
`wiki.xml.bz2`. Instead, run below code:
```console
$ mkdir src
$ wget -O src/wiki.xml.bz2 https://dumps.wikimedia.org/enwiki/20200520/enwiki-20200520-pages-articles1.xml-p1p30303.bz2
```
After downloading the dump file, we need to setup the configuration file.
Create ``expanda.cfg`` file and write the below:
```ini
[expanda.ext.wikipedia]
num-cores           = 6

[tokenization]
unk-token           = <unk>
control-tokens      = <s>
                      </s>
                      <pad>

[build]
input-files         =
    --expanda.ext.wikipedia     src/wiki.xml.bz2
```
The current directory structure of `workspace` should be as follows:
```
workspace
├── src
│   └── wiki.xml.bz2
└── expanda.cfg
```
Now we are ready to build! Run Expanda by using:
```console
$ expanda build
```
Then we can get the below output:
```
[*] execute extension [expanda.ext.wikipedia] for [src/wiki.xml.bz2]
[nltk_data] Downloading package punkt to /home/user/nltk_data...
[nltk_data]   Unzipping tokenizers/punkt.zip.
[*] merge extracted texts.
[*] start shuffling merged corpus...
[*] optimum stride: 17, buckets: 34
[*] create temporary bucket files.
[*] successfully shuffle offsets. total offsets: 102936
[*] shuffle input file: 100%|████████████████████| 102936/102936 [00:02<00:00, 34652.03it/s]
[*] start copying buckets to the output file.
[*] finish copying buckets. remove the buckets...
[*] complete preparing corpus. start training tokenizer...
[00:00:59] Reading files                            ████████████████████                 100
[00:00:04] Tokenize words                           ████████████████████ 405802   /   405802
[00:00:00] Count pairs                              ████████████████████ 405802   /   405802
[00:00:01] Compute merges                           ████████████████████ 6332     /     6332

[*] create tokenized corpus.
[*] tokenize corpus: 100%|█████████████████████| 1749902/1749902 [00:28<00:00, 61958.55it/s]
[*] split the corpus into train and test dataset.
[*] remove temporary directory.
[*] finish building corpus.
```
If you build dataset successfully, you can get the following directory tree:
```
workspace
├── build
│   ├── corpus.raw.txt
│   ├── corpus.train.txt
│   ├── corpus.test.txt
│   └── vocab.txt
├── src
│   └── wiki.xml.bz2
└── expanda.cfg
```

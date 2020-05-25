# Expanda

**The universial integrated corpus-building environment.**

![build](https://github.com/affjljoo3581/Expanda/workflows/build/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/expanda/badge/?version=latest)](https://expanda.readthedocs.io/en/latest/?badge=latest)
![GitHub](https://img.shields.io/github/license/affjljoo3581/Expanda)
[![codecov](https://codecov.io/gh/affjljoo3581/Expanda/branch/master/graph/badge.svg)](https://codecov.io/gh/affjljoo3581/Expanda)
[![CodeFactor](https://www.codefactor.io/repository/github/affjljoo3581/expanda/badge)](https://www.codefactor.io/repository/github/affjljoo3581/expanda)

## Introduction
**Expanda** is an **integrated corpus-building environment**. Expanda provides
integrated pipelines for building corpus dataset. Building corpus dataset
requires several complicated pipelines such as parsing, shuffling and
tokenization. If the corpora are gathered from different applications, it would
be a problem to parse various formats. Expanda helps to build corpus simply at
once by setting build configuration.

## Main Features
* Easy to build, simple for adding new extensions
* Manages build environment systemically
* Fast build through performance optimization (even written in Python)
* Supports multi-processing
* Extremely less memory usage
* Don't need to write new codes for each corpus. Just write one line for adding
  new corpus.

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
Let's build **Wikipedia** dataset by using Expanda. First of all, install Expanda.
```console
$ pip install expanda
```
Next, create workspace to build dataset by running:
```console
$ mkdir workspace
$ cd workspace
```
Then, download wikipedia dump file from [here](https://dumps.wikimedia.org/).
In this example, we are going to test with [part of enwiki](https://dumps.wikimedia.org/enwiki/20200520/enwiki-20200520-pages-articles1.xml-p1p30303.bz2).
Download through web browser and move to the workspace directory or, run below
code:
```console
$ wget https://dumps.wikimedia.org/enwiki/20200520/enwiki-20200520-pages-articles1.xml-p1p30303.bz2
```
For using Expanda, we need to setup the configuration file. Create
``expanda.cfg`` file and write the below:
```ini

```
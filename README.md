# Expanda

**The integrated corpus-building environment.**

![Python package](https://github.com/affjljoo3581/Expanda/workflows/Python%20package/badge.svg)
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

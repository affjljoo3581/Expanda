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
tokenizations. If the corpora are gathered from different applications, it also
be a problem to parse various formats. Expanda helps to build corpus simply at
once by setting build configuration.

Modules
----------
.. toctree::
   :maxdepth: 1

   expanda.shuffling
   expanda.tokenization
   expanda.extension

.. _`extensions`:

Extensions
----------
.. toctree::
   :maxdepth: 1

   expanda.ext.wikipedia
   expanda.ext.namuwiki


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. _`tokenization`:

expanda.tokenization
====================
.. currentmodule:: expanda.tokenization

Introduction
~~~~~~~~~~~~
Traditionally, it was believed that words -- units of language -- cannot be
split in machine learning. Sometimes words are decomposed into characters in
some cases, but major models use word-level approaches. Of course, the
approaches worked well. Even today, there is no problem to solve simple natural
language tasks through word-level based models.

However, in deep learning, the number of words in corpus is immensely
increased. Compared to traditional machine learning, deep learning treats
more general problems, and hence, contents from various categories are used and
it eventually leads growth of words.

Why the amount of words actually matters? Before discussing that, we need to
understand how to treat words as  **computable components**. There are many
ways to encode a word to vector (which is one of the computable forms). The
simplest and well-known method is `One-Hot Encoding`. It deals word as a basis
vector. For instance, the words are mapped as follows:
:math:`\text{apple} = (1, 0, 0)`, :math:`\text{banana} = (0, 1, 0)` and
:math:`\text{orange} = (0, 0, 1)`. It is intuitive and easy to implement. It
does not even require any pretrainings Each vector, however, does not contain
contextual semantics of the corresponding word. Moreover, because the vectors
are independent of each other, the size of vectors follows :math:`O(n^2)`.

So an alternative method has been recommended. Since the dimensionality of each
vector was the matter, the method suggests using **fixed dimensional vectors**
in embedding. The vectors are randomly initialized at first and then trained
with other parameters. Fixed dimensionality reduces the space complexity to
:math:`O(n)`.

In fact, fixed embedding is theoretically the same as `One-Hot Encoding` in
usual cases. In terms of linear algebra, it holds that

.. math::
    \newcommand{\M}{\mathcal{M}}
    \newcommand{\x}{\boldsymbol{x}}
    \newcommand{\e}{\boldsymbol{e}}
    \M(\x_i) = \hat{\M}(E \x_i) = \hat{\M}(\e_i)

where :math:`\M` is a neural network with feed-forward layer
:math:`E = [ \e_1, \e_2, \cdots, \e_V ]` where :math:`\e_i \in \mathbb{R}^D`,
and :math:`\x_i \in \{0, 1\}^V` is a standard basis vector of which elements
are all zero, except :math:`i`\th index that equals 1. :math:`V` and :math:`D`
imply vocabulary size and dimensionality of the model respectively. We can
interpret :math:`\e_i` as a fixed dimensional embedding vector of :math:`i`\th
word in vocabulary.

Yet, it is insufficient for extremly large corpus. The large corpus has
numerous words and the embedding vectors still possess almost of memory. The
last way to decrease memory is to decrease vocabulary size. Similar to the case
of embedding, we can consider **fixing the number of words**. If words can be
split into sub-words such as morphemes, so the similar parts of the words would
be reused, then the vocabulary size would be reduced effectively by
constructing vocabulary with those subwords.

Then, how can we tokenize words into their subwords? Actually, subword
tokenization is quite fickle, ambiguous and arbitrary. There are many
approaches to split words into their subwords. BPE (Byte-Pair Encoding) ([#]_),
Unigram LM ([#]_) and WordPiece Model ([#]_) are representatives. They are all
used in subword tokenization and perform well. Although there is a little
difference in performance between them, it does not affect the overall
performance of model.

In this module, we use *WordPiece Model* which is implemented in
`HuggingFace Tokenizers`_. Thanks to *tokenizers*, this module provides
training *WordPiece Model* and tokenizing the whole corpus into subwords. You
can use those functions by importing this module or, simply try in command
line. See `Command-line Usage`_.


Functions
~~~~~~~~~
.. autofunction:: train_tokenizer
.. autofunction:: tokenize_corpus

Command-line Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: console

    usage: expanda-tokenization train [-h] [--tmp TMP] [--subset_size SUBSET_SIZE]
                                      [--vocab_size VOCAB_SIZE]
                                      [--unk_token UNK_TOKEN]
                                      [--control_tokens [CONTROL_TOKENS [CONTROL_TOKENS ...]]]
                                      input [vocab]

    positional arguments:
      input
      vocab                 output vocabulary file

    optional arguments:
      -h, --help            show this help message and exit
      --tmp TMP             temporary directory path
      --subset_size SUBSET_SIZE
                            maximum number of lines in subset
      --vocab_size VOCAB_SIZE
                            number of subwords in vocabulary
      --unk_token UNK_TOKEN
                            unknown token name
      --control_tokens [CONTROL_TOKENS [CONTROL_TOKENS ...]]
                            control token names except unknown token

.. code-block:: console

    usage: expanda.tokenization tokenize [-h] [--unk_token UNK_TOKEN]
                                         [--control_tokens [CONTROL_TOKENS [CONTROL_TOKENS ...]]]
                                         input output vocab

    positional arguments:
      input
      output
      vocab

    optional arguments:
      -h, --help            show this help message and exit
      --unk_token UNK_TOKEN
                            unknown token name
      --control_tokens [CONTROL_TOKENS [CONTROL_TOKENS ...]]
                            control token names except unknown token

References
~~~~~~~~~~
.. [#] Philip Gage in a February 1994 article "A New Algorithm for Data Compression" in the C Users Journal.
.. [#] T\. Kudo. 2018. "Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates"
.. [#] Y\. Wu et al. 2016. "Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation"
.. _`HuggingFace Tokenizers`: https://github.com/huggingface/tokenizers

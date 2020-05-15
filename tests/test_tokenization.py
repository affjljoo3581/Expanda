from expanda.tokenization import train_tokenizer, tokenize_corpus
import tempfile
import os


_dummy_corpus = (
    'Wikipedia is a multilingual online encyclopedia created and maintained as'
    ' an open collaboration project by a community of volunteer editors, using'
    ' a wiki-based editing system. It is the largest and most popular general'
    ' reference work on the World Wide Web, and is one of the 20 most popular'
    ' websites ranked by Alexa, as of March 2020. It features exclusively free'
    ' content and no commercial ads and is owned and supported by the'
    ' Wikimedia Foundation, a non-profit organization funded primarily through'
    ' donations.\n'
    'Wikipedia was launched on January 15, 2001, by Jimmy Wales and Larry'
    ' Sanger. Sanger coined its name, as a portmanteau of "wiki" (the Hawaiian'
    ' word for "quick") and "encyclopedia". Initially an English-language'
    ' encyclopedia, versions of Wikipedia in other languages were quickly'
    ' developed. With 6.1 million articles, the English Wikipedia is the'
    ' largest of the more than 300 Wikipedia encyclopedias. Overall, Wikipedia'
    ' comprises more than 53 million articles attracting 1.5 billion unique'
    ' visitors per month.\n'
    'In 2005, Nature published a peer review comparing 42 hard science'
    ' articles from Encyclopædia Britannica and Wikipedia and found that'
    ' Wikipedia\'s level of accuracy approached that of Britannica, although'
    ' critics suggested that it might not have fared so well in a similar'
    ' study of a random sampling of all articles or one focused on social'
    ' science or contentious social issues. The following year, Time magazine'
    ' stated that the open-door policy of allowing anyone to edit had made'
    ' Wikipedia the biggest and possibly the best encyclopedia in the world,'
    ' and was a testament to the vision of Jimmy Wales.\n'
    'Wikipedia has been criticized for exhibiting systemic bias, for'
    ' presenting a mixture of "truth, half truth, and some falsehoods", and'
    ' for being subject to manipulation and spin in controversial topics.'
    ' Wikipedia has also been criticized for gender bias, particularly on its'
    ' English-language site, where the dominant majority of editors are male.'
    ' However, edit-a-thons have been held to encourage female editors and'
    ' increase the coverage of women\'s topics. Facebook announced that by'
    ' 2017 it would help readers detect fake news by suggesting links to'
    ' related Wikipedia articles. YouTube announced a similar plan in 2018.')


def test_training_tokenizer_well():
    # Use temporary directory since `tokenizers` does not support mocking.
    input_file = os.path.join(tempfile.gettempdir(), 'input')
    vocab_file = os.path.join(tempfile.gettempdir(), 'vocab')

    # Write dummy corpus file to `input_file`.
    with open(input_file, 'w') as fp:
        fp.write(_dummy_corpus)

    # Train tokenizer with dummy corpus file.
    train_tokenizer(input_file,
                    vocab_file,
                    tempfile.gettempdir(),
                    vocab_size=100)

    # Check that the tokenizer is trained well.
    with open(vocab_file, 'r') as fp:
        assert len(fp.readlines()) == 100

    # Remove created temporary files.
    os.remove(input_file)
    os.remove(vocab_file)


def test_tokenizing_corpus_well():
    # Use temporary directory since `tokenizers` does not support mocking.
    input_file = os.path.join(tempfile.gettempdir(), 'input')
    vocab_file = os.path.join(tempfile.gettempdir(), 'vocab')
    output_file = os.path.join(tempfile.gettempdir(), 'output')

    # Write dummy corpus file to `input_file`.
    with open(input_file, 'w') as fp:
        fp.write(_dummy_corpus)

    # First of all, train the tokenizer to tokenize corpus.
    train_tokenizer(input_file,
                    vocab_file,
                    tempfile.gettempdir(),
                    vocab_size=100)

    # Next, tokenize the given corpus by using trained tokenizer.
    tokenize_corpus(input_file, output_file, vocab_file)

    # Check the corpus is tokenized well.
    with open(output_file, 'r') as fp:
        assert fp.read().strip().count('\n') == _dummy_corpus.count('\n')

    # Remove created temporary files.
    os.remove(vocab_file)
    os.remove(input_file)

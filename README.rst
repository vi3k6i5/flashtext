
synonym-extractor
==============

Synonym Extractor is a python library that is loosely based on `Aho-Corasick algorithm
<https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm>`_.

The idea is to extract words that we care about from a given sentence in one pass.

Basically say I have a vocabulary of 10K words and I want to get all the words from that set present in a sentence. A simple regex match will take a lot of time to loop over the 10K documents.

Hence we use a simpler yet much faster algorithm to get the desired result.

Installation
-------
::

    pip install flashtext

Usage
------
::
    
    # import module
    from synonym.extractor import SynonymExtractor

    # Create an object of SynonymExtractor
    synonym_extractor = SynonymExtractor()

    # add synonyms
    synonym_names = ['NY', 'new-york', 'SF']
    clean_names = ['new york', 'new york', 'san francisco']

    for synonym_name, clean_name in zip(synonym_names, clean_names):
        synonym_extractor.add_to_synonym(synonym_name, clean_name)

    synonyms_found = synonym_extractor.get_synonyms_from_sentence('I love SF and NY. new-york is the best.')

    synonyms_found
    >> ['san francisco', 'new york', 'new york']


Algorithm
----------

synonym-extractor is based on `Aho-Corasick algorithm
<https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm>`_.

Documentation
----------

Documentation can be found at `Read the Docs
<http://synonym-extractor.readthedocs.org>`_.


Why
------

::

Say you have a corpus where similar words appear frequently.

eg: Last weekened I was in NY.
    I am traveling to new york next weekend.

If you train a word2vec model on this or do any sort of NLP it will treat NY and new york as 2 different words. 

Instead if you create a synonym dictionary like:

eg: NY=>new york
    new york=>new york

Then you can extract NY and new york as the same text.

To do the same with regex it will take a lot of time:

============  ========== = =========  ============
Docs count    # Synonyms : Regex      synonym-extractor
============  ========== = =========  ============
1.5 million   2K         : 16 hours   NA
2.5 million   10K        : 15 days    15 mins
============  ========== = =========  ============

The idea for this library came from the following `StackOverflow question
<https://stackoverflow.com/questions/44178449/regex-replace-is-taking-time-for-millions-of-documents-how-to-make-it-faster>`_.


License
-------

The project is licensed under the MIT license.

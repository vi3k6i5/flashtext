.. FlashText documentation master file, created by
   sphinx-quickstart on Wed Aug 16 22:47:29 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FlashText's documentation!
=====================================


Installation
------------
::

    $ pip install flashtext

Usage
-----
Extract keywords
    >>> from flashtext.keyword import KeywordProcessor
    >>> keyword_processor = KeywordProcessor()
    >>> keyword_processor.add_keyword('Big Apple', 'New York')
    >>> keyword_processor.add_keyword('Bay Area')
    >>> keywords_found = keyword_processor.extract_keywords('I love Big Apple and Bay Area.')
    >>> keywords_found
    >>> ['New York', 'Bay Area']

Replace keywords
    >>> keyword_processor.add_keyword('New Delhi', 'NCR region')
    >>> new_sentence = keyword_processor.replace_keywords('I love Big Apple and new delhi.')
    >>> new_sentence
    >>> 'I love New York and NCR region.'

Case Sensitive example
    >>> from flashtext.keyword import KeywordProcessor
    >>> keyword_processor = KeywordProcessor(case_sensitive=True)
    >>> keyword_processor.add_keyword('Big Apple', 'New York')
    >>> keyword_processor.add_keyword('Bay Area')
    >>> keywords_found = keyword_processor.extract_keywords('I love big Apple and Bay Area.')
    >>> keywords_found
    >>> ['Bay Area']

No clean name for Keywords
    >>> from flashtext.keyword import KeywordProcessor
    >>> keyword_processor = KeywordProcessor()
    >>> keyword_processor.add_keyword('Big Apple')
    >>> keyword_processor.add_keyword('Bay Area')
    >>> keywords_found = keyword_processor.extract_keywords('I love big Apple and Bay Area.')
    >>> keywords_found
    >>> ['Big Apple', 'Bay Area']

API doc
-------


.. toctree::
    :maxdepth: 2
    :caption: KeywordProcessor

    api
    keyword_processor


Why not Regex?
--------------

It's a custom algorithm based on `Aho-Corasick algorithm
<https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm>`_ and `Trie Dictionary
<https://en.wikipedia.org/wiki/Trie Dictionary>`_.


To do the same with regex it will take a lot of time:

============  ========== = =========  ============
Docs count    # Keywords : Regex      flashtext
============  ========== = =========  ============
1.5 million   2K         : 16 hours   NA
2.5 million   10K        : 15 days    15 mins
============  ========== = =========  ============

The idea for this library came from the following `StackOverflow question
<https://stackoverflow.com/questions/44178449/regex-replace-is-taking-time-for-millions-of-documents-how-to-make-it-faster>`_.

Contribute
----------

- Issue Tracker: https://github.com/vi3k6i5/flashtext/issues
- Source Code: https://github.com/vi3k6i5/flashtext/


License
-------

The project is licensed under the MIT license.

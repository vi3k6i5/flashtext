=========
FlashText
=========

.. image:: https://readthedocs.org/projects/flashtext/badge/?version=latest
   :target: http://flashtext.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


[![Documentation Status](https://readthedocs.org/projects/flashtext/badge/?version=latest)](http://flashtext.readthedocs.io/en/latest/?badge=latest)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/vi3k6i5/flashtext/blob/master/LICENSE)

Installation
------------
::

    $ pip install flashtext

Usage
-----
Simple example
    >>> from flashtext.keyword import KeywordProcessor
    >>> keyword_processor = KeywordProcessor()
    >>> keyword_processor.add_keyword('Big Apple', 'New York')
    >>> keyword_processor.add_keyword('Bay Area')
    >>> keywords_found = keyword_processor.extract_keywords('I love Big Apple and Bay Area.')
    >>> keywords_found
    >>> ['New York', 'Bay Area']

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

Documentation can be found at `FlashText Read the Docs
<http://flashtext.readthedocs.io/>`_.

Contribute
----------

- Issue Tracker: https://github.com/vi3k6i5/flashtext/issues
- Source Code: https://github.com/vi3k6i5/flashtext/


License
-------

The project is licensed under the MIT license.

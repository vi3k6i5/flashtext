from collections import defaultdict
from flashtext import KeywordProcessor
import logging
import unittest
import json
import re

logger = logging.getLogger(__name__)


class TestKPDictionaryLikeFeatures(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")

    def tearDown(self):
        logger.info("Ending.")

    def test_term_in_dictionary(self):
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keyword('j2ee', 'Java')
        keyword_processor.add_keyword('colour', 'color')
        keyword_processor.get_keyword('j2ee')
        self.assertEqual(keyword_processor.get_keyword('j2ee'),
                         'Java',
                         "get_keyword didn't return expected Keyword")
        self.assertEqual(keyword_processor['colour'],
                         'color',
                         "get_keyword didn't return expected Keyword")
        self.assertEqual(keyword_processor['Test'],
                         None,
                         "get_keyword didn't return expected Keyword")
        self.assertTrue('colour' in keyword_processor,
                        "get_keyword didn't return expected Keyword")
        self.assertFalse('Test' in keyword_processor,
                         "get_keyword didn't return expected Keyword")

    def test_term_in_dictionary_case_sensitive(self):
        keyword_processor = KeywordProcessor(case_sensitive=True)
        keyword_processor.add_keyword('j2ee', 'Java')
        keyword_processor.add_keyword('colour', 'color')
        keyword_processor.get_keyword('j2ee')
        self.assertEqual(keyword_processor.get_keyword('j2ee'),
                         'Java',
                         "get_keyword didn't return expected Keyword")
        self.assertEqual(keyword_processor['colour'],
                         'color',
                         "get_keyword didn't return expected Keyword")
        self.assertEqual(keyword_processor['J2ee'],
                         None,
                         "get_keyword didn't return expected Keyword")
        self.assertTrue('colour' in keyword_processor,
                        "get_keyword didn't return expected Keyword")
        self.assertFalse('Colour' in keyword_processor,
                         "get_keyword didn't return expected Keyword")


if __name__ == '__main__':
    unittest.main()

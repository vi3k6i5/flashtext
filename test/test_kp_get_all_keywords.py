from collections import defaultdict
from flashtext import KeywordProcessor
import logging
import unittest
import json
import re

logger = logging.getLogger(__name__)


class TestKPGetAllKeywords(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")

    def tearDown(self):
        logger.info("Ending.")

    def test_get_all_keywords(self):
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keyword('j2ee', 'Java')
        keyword_processor.add_keyword('colour', 'color')
        keyword_processor.get_all_keywords()
        self.assertEqual(keyword_processor.get_all_keywords(),
                         {'colour': 'color', 'j2ee': 'Java'},
                         "get_all_keywords didn't match expected results.")


if __name__ == '__main__':
    unittest.main()

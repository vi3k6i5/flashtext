from collections import defaultdict
from flashtext import KeywordProcessor
import logging
import unittest
import pytest
import json
import re

logger = logging.getLogger(__name__)


class TestKPExceptions(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")

    def tearDown(self):
        logger.info("Ending.")

    def test_iterator_NotImplementedError(self):
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keyword('j2ee', 'Java')
        keyword_processor.add_keyword('colour', 'color')
        keyword_processor.get_all_keywords()
        with pytest.raises(NotImplementedError):
            for value in keyword_processor:
                pass

    def test_add_keyword_file_missing(self):
        keyword_processor = KeywordProcessor()
        with pytest.raises(IOError):
            keyword_processor.add_keyword_from_file('missing_file')

    def test_add_keyword_from_list(self):
        keyword_processor = KeywordProcessor()
        keyword_list = "java"
        with pytest.raises(AttributeError):
            keyword_processor.add_keywords_from_list(keyword_list)

    def test_add_keyword_from_dictionary(self):
        keyword_processor = KeywordProcessor()
        keyword_dict = {
            "java": "java_2e",
            "product management": "product manager"
        }
        with pytest.raises(AttributeError):
            keyword_processor.add_keywords_from_dict(keyword_dict)

    def test_remove_keyword_from_list(self):
        keyword_processor = KeywordProcessor()
        keyword_list = "java"
        with pytest.raises(AttributeError):
            keyword_processor.remove_keywords_from_list(keyword_list)

    def test_remove_keyword_from_dictionary(self):
        keyword_processor = KeywordProcessor()
        keyword_dict = {
            "java": "java_2e",
            "product management": "product manager"
        }
        with pytest.raises(AttributeError):
            keyword_processor.remove_keywords_from_dict(keyword_dict)

    def test_empty_string(self):
        keyword_processor = KeywordProcessor()
        keyword_dict = {
            "java": "java_2e",
            "product management": "product manager"
        }
        self.assertEqual(keyword_processor.extract_keywords(""), [],
                         "new_sentence don't match the expected result")
        self.assertEqual(keyword_processor.replace_keywords(""), "",
                         "new_sentence don't match the expected result")

if __name__ == '__main__':
    unittest.main()

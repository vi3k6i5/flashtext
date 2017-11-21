from collections import defaultdict
from flashtext import KeywordProcessor
import logging
import unittest
import json
import re

logger = logging.getLogger(__name__)


class TestKeywordRemover(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")
        with open('test/keyword_remover_test_cases.json') as f:
            self.test_cases = json.load(f)

    def tearDown(self):
        logger.info("Ending.")

    def test_remove_keywords(self):
        """For each of the test case initialize a new KeywordProcessor.
        Add the keywords the test case to KeywordProcessor.
        Remove the keywords in remove_keyword_dict
        Extract keywords and check if they match the expected result for the test case.
        """
        for test_id, test_case in enumerate(self.test_cases):
            keyword_processor = KeywordProcessor()
            keyword_processor.add_keywords_from_dict(test_case['keyword_dict'])
            keyword_processor.remove_keywords_from_dict(test_case['remove_keyword_dict'])
            keywords_extracted = keyword_processor.extract_keywords(test_case['sentence'])
            self.assertEqual(keywords_extracted, test_case['keywords'],
                             "keywords_extracted don't match the expected results for test case: {}".format(test_id))

    def test_remove_keywords_using_list(self):
        """For each of the test case initialize a new KeywordProcessor.
        Add the keywords the test case to KeywordProcessor.
        Remove the keywords in remove_keyword_dict
        Extract keywords and check if they match the expected result for the test case.
        """
        for test_id, test_case in enumerate(self.test_cases):
            keyword_processor = KeywordProcessor()
            keyword_processor.add_keywords_from_dict(test_case['keyword_dict'])
            for key in test_case['remove_keyword_dict']:
                keyword_processor.remove_keywords_from_list(test_case['remove_keyword_dict'][key])
            keywords_extracted = keyword_processor.extract_keywords(test_case['sentence'])
            self.assertEqual(keywords_extracted, test_case['keywords'],
                             "keywords_extracted don't match the expected results for test case: {}".format(test_id))

    def test_remove_keywords_dictionary_compare(self):
        """For each of the test case initialize a new KeywordProcessor.
        Add the keywords the test case to KeywordProcessor.
        Remove the keywords in remove_keyword_dict
        Extract keywords and check if they match the expected result for the test case.
        """
        for test_id, test_case in enumerate(self.test_cases):
            keyword_processor = KeywordProcessor()
            keyword_processor.add_keywords_from_dict(test_case['keyword_dict'])
            keyword_processor.remove_keywords_from_dict(test_case['remove_keyword_dict'])
            keyword_trie_dict = keyword_processor.keyword_trie_dict

            new_dictionary = defaultdict(list)
            for key, values in test_case['keyword_dict'].items():
                for value in values:
                    if not(key in test_case['remove_keyword_dict'] and value in test_case['remove_keyword_dict'][key]):
                        new_dictionary[key].append(value)

            keyword_processor_two = KeywordProcessor()
            keyword_processor_two.add_keywords_from_dict(new_dictionary)
            keyword_trie_dict_two = keyword_processor_two.keyword_trie_dict
            self.assertTrue(keyword_trie_dict == keyword_trie_dict_two,
                            "keywords_extracted don't match the expected results for test case: {}".format(test_id))
if __name__ == '__main__':
    unittest.main()

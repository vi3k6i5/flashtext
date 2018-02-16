from collections import defaultdict
from flashtext import KeywordProcessor
import logging
import unittest
import json
import re
import sys

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class TestKPLen(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")
        with open('test/keyword_remover_test_cases.json') as f:
            self.test_cases = json.load(f)

    def tearDown(self):
        logger.info("Ending.")

    def test_remove_keywords_dictionary_len(self):
        """For each of the test case initialize a new KeywordProcessor.
        Add the keywords the test case to KeywordProcessor.
        Remove the keywords in remove_keyword_dict
        Extract keywords and check if they match the expected result for the test case.
        """
        for test_id, test_case in enumerate(self.test_cases):
            keyword_processor = KeywordProcessor()
            keyword_processor.add_keywords_from_dict(test_case['keyword_dict'])
            keyword_processor.remove_keywords_from_dict(test_case['remove_keyword_dict'])

            kp_len = len(keyword_processor)

            new_dictionary = defaultdict(list)
            for key, values in test_case['keyword_dict'].items():
                for value in values:
                    if not(key in test_case['remove_keyword_dict'] and value in test_case['remove_keyword_dict'][key]):
                        new_dictionary[key].append(value)

            keyword_processor_two = KeywordProcessor()
            keyword_processor_two.add_keywords_from_dict(new_dictionary)
            kp_len_two = len(keyword_processor_two)
            self.assertEqual(kp_len, kp_len_two,
                             "keyword processor length doesn't match for Text ID {}".format(test_id))
if __name__ == '__main__':
    unittest.main()

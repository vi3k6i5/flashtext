from flashtext import KeywordProcessor
import logging
import unittest
import json

logger = logging.getLogger(__name__)


class TestKeywordExtractor(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")
        with open('test/keyword_extractor_test_cases.json') as f:
            self.test_cases = json.load(f)

    def tearDown(self):
        logger.info("Ending.")

    def test_extract_keywords(self):
        """For each of the test case initialize a new KeywordProcessor.
        Add the keywords the test case to KeywordProcessor.
        Extract keywords and check if they match the expected result for the test case.

        """
        for test_id, test_case in enumerate(self.test_cases):
            keyword_processor = KeywordProcessor()
            keyword_processor.add_keywords_from_dict(test_case['keyword_dict'])
            keywords_extracted = keyword_processor.extract_keywords(test_case['sentence'])
            self.assertEqual(keywords_extracted, test_case['keywords'],
                             "keywords_extracted don't match the expected results for test case: {}".format(test_id))

    def test_extract_keywords_case_sensitive(self):
        """For each of the test case initialize a new KeywordProcessor.
        Add the keywords the test case to KeywordProcessor.
        Extract keywords and check if they match the expected result for the test case.

        """
        for test_id, test_case in enumerate(self.test_cases):
            keyword_processor = KeywordProcessor(case_sensitive=True)
            keyword_processor.add_keywords_from_dict(test_case['keyword_dict'])
            keywords_extracted = keyword_processor.extract_keywords(test_case['sentence'])
            self.assertEqual(keywords_extracted, test_case['keywords_case_sensitive'],
                             "keywords_extracted don't match the expected results for test case: {}".format(test_id))

if __name__ == '__main__':
    unittest.main()

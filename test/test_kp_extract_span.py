from flashtext import KeywordProcessor
import logging
import unittest
import json

logger = logging.getLogger(__name__)


class TestKPExtractorSpan(unittest.TestCase):
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
            for key in test_case['keyword_dict']:
                keyword_processor.add_keywords_from_list(test_case['keyword_dict'][key])
            keywords_extracted = keyword_processor.extract_keywords(test_case['sentence'], span_info=True)
            for kwd in keywords_extracted:
                # returned keyword lowered should match the sapn from sentence
                self.assertEqual(
                    kwd[0].lower(), test_case['sentence'].lower()[kwd[1]:kwd[2]],
                    "keywords span don't match the expected results for test case: {}".format(test_id))

    def test_extract_keywords_case_sensitive(self):
        """For each of the test case initialize a new KeywordProcessor.
        Add the keywords the test case to KeywordProcessor.
        Extract keywords and check if they match the expected result for the test case.

        """
        for test_id, test_case in enumerate(self.test_cases):
            keyword_processor = KeywordProcessor(case_sensitive=True)
            for key in test_case['keyword_dict']:
                keyword_processor.add_keywords_from_list(test_case['keyword_dict'][key])
            keywords_extracted = keyword_processor.extract_keywords(test_case['sentence'], span_info=True)
            for kwd in keywords_extracted:
                # returned keyword should match the sapn from sentence
                self.assertEqual(
                    kwd[0], test_case['sentence'][kwd[1]:kwd[2]],
                    "keywords span don't match the expected results for test case: {}".format(test_id))

if __name__ == '__main__':
    unittest.main()

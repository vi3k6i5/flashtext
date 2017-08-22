from flashtext.keyword import KeywordProcessor
import logging
import unittest
import json
import re

logger = logging.getLogger(__name__)


class TestKeywordExtractor(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")
        with open('test/keyword_extractor_test_cases.json') as f:
            self.test_cases = json.load(f)

    def tearDown(self):
        logger.info("Ending.")

    def test_replace_keywords(self):
        """For each of the test case initialize a new KeywordProcessor.
        Add the keywords the test case to KeywordProcessor.
        Replace keywords and check if they match the expected result for the test case.

        """
        for test_id, test_case in enumerate(self.test_cases):
            keyword_replacer = KeywordProcessor()
            keyword_replacer.add_keywords_from_dict(test_case['keyword_dict'])
            new_sentence = keyword_replacer.replace_keywords(test_case['sentence'])

            replaced_sentence = test_case['sentence']
            keyword_mapping = {}
            for val in test_case['keyword_dict']:
                for value in test_case['keyword_dict'][val]:
                    keyword_mapping[value] = val
            for key in sorted(keyword_mapping, key=len, reverse=True):
                if any(special_char in key for special_char in ['.', '+']):
                    replaced_sentence = replaced_sentence.replace(key, keyword_mapping[key])
                else:
                    lowercase = re.compile(r'\b' + re.escape(key) + r'\b')
                    replaced_sentence = lowercase.sub(keyword_mapping[key], replaced_sentence)

            self.assertEqual(new_sentence, replaced_sentence,
                             "new_sentence don't match the expected results for test case: {}".format(test_id))

if __name__ == '__main__':
    unittest.main()

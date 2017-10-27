from flashtext import KeywordProcessor
import logging
import unittest
import json
import re

logger = logging.getLogger(__name__)


class TestKeywordReplacer(unittest.TestCase):
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
            # To handle issue like https://github.com/vi3k6i5/flashtext/issues/8
            # clean names are replaced with "_" in place of white space.
            for key, values in test_case['keyword_dict'].items():
                for value in values:
                    keyword_replacer.add_keyword(value, key.replace(" ", "_"))
            new_sentence = keyword_replacer.replace_keywords(test_case['sentence'])

            replaced_sentence = test_case['sentence']
            keyword_mapping = {}
            for val in test_case['keyword_dict']:
                for value in test_case['keyword_dict'][val]:
                    keyword_mapping[value] = val.replace(" ", "_")
            for key in sorted(keyword_mapping, key=len, reverse=True):
                lowercase = re.compile(r'(?<!\w){}(?!\w)'.format(re.escape(key)))
                replaced_sentence = lowercase.sub(keyword_mapping[key], replaced_sentence)

            self.assertEqual(new_sentence, replaced_sentence,
                             "new_sentence don't match the expected results for test case: {}".format(test_id))

if __name__ == '__main__':
    unittest.main()

from flashtext import KeywordProcessor
import logging
import unittest
import json

logger = logging.getLogger(__name__)


class TestFileLoad(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")

    def tearDown(self):
        logger.info("Ending.")

    def test_file_format_one(self):
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keyword_from_file('test/keywords_format_one.txt')
        sentence = 'I know java_2e and product management techniques'
        keywords_extracted = keyword_processor.extract_keywords(sentence)
        self.assertEqual(keywords_extracted, ['java', 'product management'],
                         "Failed file format one test")
        sentence_new = keyword_processor.replace_keywords(sentence)
        self.assertEqual(sentence_new, "I know java and product management",
                         "Failed file format one test")

    def test_file_format_two(self):
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keyword_from_file('test/keywords_format_two.txt')
        sentence = 'I know java and product management'
        keywords_extracted = keyword_processor.extract_keywords(sentence)
        self.assertEqual(keywords_extracted, ['java', 'product management'],
                         "Failed file format one test")
        sentence_new = keyword_processor.replace_keywords(sentence)
        self.assertEqual(sentence_new, "I know java and product management",
                         "Failed file format one test")

if __name__ == '__main__':
    unittest.main()

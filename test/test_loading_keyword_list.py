from flashtext import KeywordProcessor
import logging
import unittest
import json

logger = logging.getLogger(__name__)


class TestListLoad(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")

    def tearDown(self):
        logger.info("Ending.")

    def test_list_loading(self):
        keyword_processor = KeywordProcessor()
        keyword_list = ["java", "product management"]
        keyword_processor.add_keywords_from_list(keyword_list)
        sentence = 'I know java and product management'
        keywords_extracted = keyword_processor.extract_keywords(sentence)
        self.assertEqual(keywords_extracted, ['java', 'product management'],
                         "Failed file format one test")
        sentence_new = keyword_processor.replace_keywords(sentence)
        self.assertEqual(sentence_new, "I know java and product management",
                         "Failed file format one test")

if __name__ == '__main__':
    unittest.main()

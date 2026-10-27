from flashtext import KeywordProcessor
import logging
import unittest
import json
import io
import os
import tempfile

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

    def test_clean_name_contains_separator(self):
        for clean_name in ('left=>right', 'one=>two=>three'):
            fd, path = tempfile.mkstemp()
            os.close(fd)
            try:
                with io.open(path, 'w', encoding='utf-8') as stream:
                    stream.write('keyword=>' + clean_name + '\n')
                processor = KeywordProcessor()
                processor.add_keyword_from_file(path)
                self.assertEqual(processor.extract_keywords('keyword'), [clean_name])
                self.assertEqual(processor.replace_keywords('a keyword here'), 'a ' + clean_name + ' here')
            finally:
                os.remove(path)

if __name__ == '__main__':
    unittest.main()

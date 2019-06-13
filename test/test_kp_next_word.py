from flashtext import KeywordProcessor
import logging
import unittest

logger = logging.getLogger(__name__)

class TestKPNextWord(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")

    def tearDown(self):
        logger.info("Ending.")

    def test_next_word(self):
        """
        Test for next word extraction
        """
        keyword_proc = KeywordProcessor()
        self.assertEqual(keyword_proc.get_next_word(''), '')
        self.assertEqual(keyword_proc.get_next_word('random sentence'), 'random')
        self.assertEqual(keyword_proc.get_next_word(' random sentence'), '')

if __name__ == '__main__':
    unittest.main()
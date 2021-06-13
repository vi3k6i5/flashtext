from flashtext import KeywordProcessor
import logging
import unittest

logger = logging.getLogger(__name__)

class TestReplaceFuzzy(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")

    def tearDown(self):
        logger.info("Ending.")

    def test_extract_deletion(self):
        """
        Test replace is working with an addition (cost of 1)
        """
        keyword_proc = KeywordProcessor()
        for keyword in (('skype', 'messenger'), ):
            keyword_proc.add_keyword(*keyword)

        sentence = "hello, do you have skpe ?"
        target_sentence = "hello, do you have messenger ?"
        self.assertEqual(keyword_proc.replace_keywords(sentence, max_cost=1), target_sentence)


    def test_replace_addition(self):
        """
        Test replace is working with an addition (cost of 1)
        """
        keyword_proc = KeywordProcessor()
        for keyword in (('colour here', 'couleur ici'), ('and heere', 'et ici')):
            keyword_proc.add_keyword(*keyword)

        sentence = "color here blabla and here"
        target_sentence = "couleur ici blabla et ici"
        self.assertEqual(keyword_proc.replace_keywords(sentence, max_cost=1), target_sentence)

    def test_replace_cost_spread_over_multiple_words(self):
        """
        Here we try to replace a keyword made of different words
        the current cost should be decreased by one when encountering 'maade' (1 insertion)
        and again by one when encountering 'multple' (1 deletion)
        """
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('made of multiple words', 'with only one word')
        sentence = "this sentence contains a keyword maade of multple words"
        target_sentence = "this sentence contains a keyword with only one word"
        self.assertEqual(keyword_proc.replace_keywords(sentence, max_cost=2), target_sentence)


    def test_replace_multiple_keywords(self):
        """
        Simply test if all internal variables have been reset
        by testing if we can replace multiple keywords in a row
        """
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('first keyword', '1st keyword')
        keyword_proc.add_keyword('second keyword', '2nd keyword')
        sentence = "start with a first kyword then add a secand keyword"
        target_sentence = "start with a 1st keyword then add a 2nd keyword"
        self.assertEqual(keyword_proc.replace_keywords(sentence, max_cost=1), target_sentence)


if __name__ == '__main__':
    unittest.main()
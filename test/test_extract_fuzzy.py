from flashtext import KeywordProcessor
import logging
import unittest

logger = logging.getLogger(__name__)

class TestExtractFuzzy(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")

    def tearDown(self):
        logger.info("Ending.")

    def test_extract_deletion(self):
        """
        Fuzzy deletion
        """
        keyword_proc = KeywordProcessor()
        for keyword in (('skype', 'messenger'), ):
            keyword_proc.add_keyword(*keyword)

        sentence = "hello, do you have skpe ?"
        extracted_keywords = [('messenger', 19, 23)]
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=1), extracted_keywords)


    def test_extract_addition(self):
        """
        Fuzzy addition
        """
        keyword_proc = KeywordProcessor()
        for keyword in (('colour here', 'couleur ici'), ('and heere', 'et ici')):
            keyword_proc.add_keyword(*keyword)

        sentence = "color here blabla and here"

        extracted_keywords = [('couleur ici', 0, 10), ('et ici', 18, 26)]
        self.assertListEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=1), extracted_keywords)


    def test_correct_keyword_on_addition(self):
        """
        Test for simple additions using the levensthein function
        We ensure we end up on the right node in the trie when starting from the current node
        """
        keyword_proc = KeywordProcessor()
        for keyword in (('colour here', 'couleur ici'), ('and heere', 'et ici')):
            keyword_proc.add_keyword(*keyword)

        current_dict = keyword_proc.keyword_trie_dict['c']['o']['l']['o']
        closest_node, cost, depth = next(
            keyword_proc.levensthein('r', max_cost=1, start_node=current_dict),
            ({}, 0, 0)
            )
        self.assertDictEqual(closest_node, current_dict['u']['r'])
        self.assertEqual(cost, 1)
        self.assertEqual(depth, 2)

        current_dict_continued = {'e' : {'e': {'r': {'e': {'_keyword_': 'et ici'}}}}}
        closest_node, cost, depth = next(
            keyword_proc.levensthein('ere', max_cost=1, start_node=current_dict_continued),
            ({}, 0, 0),
        )
        self.assertDictEqual(closest_node, current_dict_continued['e']['e']['r']['e'])
        self.assertEqual(cost, 1)
        self.assertEqual(depth, 4)


    def test_correct_keyword_on_deletion(self):
        """
        Test for simple deletions using the levensthein function
        We ensure we end up on the right node in the trie when starting from the current node
        """
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('skype')
        current_dict = {'y': {'p': {'e': {'_keyword_': 'skype'}}}}

        closest_node, cost, depth = next(
            keyword_proc.levensthein('pe', max_cost=1, start_node=current_dict),
            ({}, 0, 0),
        )

        self.assertDictEqual(closest_node, current_dict['y']['p']['e'])
        self.assertEqual(cost, 1)
        self.assertEqual(depth, 3)

    def test_correct_keyword_on_substitution(self):
        """
        Test for simple substitions using the levensthein function
        We ensure we end up on the right node in the trie when starting from the current node
        """
        keyword_proc = KeywordProcessor()
        for keyword in (('skype', 'messenger'),):
            keyword_proc.add_keyword(*keyword)

        current_dict = keyword_proc.keyword_trie_dict['s']['k']
        closest_node, cost, depth = next(
            keyword_proc.levensthein('ope', max_cost=1, start_node=current_dict),
            ({}, 0, 0)
            )
        self.assertDictEqual(closest_node, current_dict['y']['p']['e'])
        self.assertEqual(cost, 1)
        self.assertEqual(depth, 3)

    def test_extract_cost_spread_over_multiple_words(self):
        """
        Here we try to extract a keyword made of different words
        the current cost should be decreased by one when encountering 'maade' (1 insertion)
        and again by one when encountering 'multple' (1 deletion)
        """
        keyword_proc = KeywordProcessor()
        keyword_made_of_multiple_words = 'made of multiple words'
        keyword_proc.add_keyword(keyword_made_of_multiple_words)
        sentence = "this sentence contains a keyword maade of multple words"

        extracted_keywords = [(keyword_made_of_multiple_words, 33, 55)]
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=2), extracted_keywords)


    def test_extract_multiple_keywords(self):
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('first keyword')
        keyword_proc.add_keyword('second keyword')
        sentence = "starts with a first kyword then add a secand keyword"
        extracted_keywords = [
            ('first keyword', 14, 26),
            ('second keyword', 38, 52),
        ]
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=1), extracted_keywords)

    def test_intermediate_match(self):
        """
        In this test, we have an intermediate fuzzy match with a keyword (the shortest one)
        We first check that we extract the longest keyword if the max_cost is big enough
        Then we retry with a smaller max_cost, excluding the longest, and check that the shortest is extracted
        """
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('keyword')
        keyword_proc.add_keyword('keyword with many words')
        sentence = "This sentence contains a keywrd with many woords"

        shortest_keyword = ('keyword', 25, 31)
        longest_keyword = ('keyword with many words', 25, 48)

        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=2), [longest_keyword])
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=1), [shortest_keyword])

    def test_intermediate_match_then_no_match(self):
        """
        In this test, we have an intermediate fuzzy match with a keyword (the shortest one)
        We check that we get only the shortest keyword when going further into fuzzy match is too
        expansive to get the longest keyword. We also extract a classic match later in the string,
        to check that the inner data structures all have a correct state
        """
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('keyword')
        keyword_proc.add_keyword('keyword with many words')
        sentence = "This sentence contains a keywrd with many items inside, a keyword at the end"

        keywords = [('keyword', 25, 31), ('keyword', 58, 65)]
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=2), keywords)


if __name__ == '__main__':
    unittest.main()
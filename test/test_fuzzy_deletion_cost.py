from flashtext import KeywordProcessor
import unittest


class TestFuzzyDeletionCost(unittest.TestCase):
    def test_empty_input_candidates_charge_deleted_characters(self):
        for keyword in ('a', 'cat', 'word'):
            with self.subTest(keyword=keyword):
                processor = KeywordProcessor()
                processor.add_keyword(keyword, 'MATCH')
                self.assertEqual(list(processor.levensthein('', max_cost=len(keyword) - 1)), [])
                candidates = list(processor.levensthein('', max_cost=len(keyword)))
                self.assertEqual(candidates, [({'_keyword_': 'MATCH'}, len(keyword), len(keyword))])

    def test_missing_word_and_substitution_share_budget(self):
        for case_sensitive in (False, True):
            with self.subTest(case_sensitive=case_sensitive):
                processor = KeywordProcessor(case_sensitive=case_sensitive)
                processor.add_keyword('x cat dog', 'MATCH')
                self.assertEqual(processor.extract_keywords('x  dag', max_cost=3), [])
                self.assertEqual(processor.replace_keywords('x  dag', max_cost=3), 'x  dag')
                self.assertEqual(
                    processor.extract_keywords('x  dag', span_info=True, max_cost=4),
                    [('MATCH', 0, 6)],
                )
                self.assertEqual(processor.replace_keywords('x  dag', max_cost=4), 'MATCH')
                self.assertEqual(processor.extract_keywords('x  dog', max_cost=3), ['MATCH'])
                self.assertEqual(processor.replace_keywords('x  dog', max_cost=3), 'MATCH')

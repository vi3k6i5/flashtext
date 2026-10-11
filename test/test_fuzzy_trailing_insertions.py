import unittest

from flashtext import KeywordProcessor


class TestFuzzyTrailingInsertions(unittest.TestCase):
    def test_trailing_insertions(self):
        cases = [
            ('cat', 'cats', 'CAT', 1),
            ('cat', 'catxy', 'CAT', 2),
            ('cat dog', 'cats dog', 'CAT', 1),
            ('cat dog', 'cat dogs', 'CAT', 1),
            ('cat dog', 'cats dogs', 'CAT', 2),
        ]
        for keyword, text, replacement, cost in cases:
            for case_sensitive in (False, True):
                for suffix in ('', ' !'):
                    with self.subTest(keyword=keyword, text=text, suffix=suffix,
                                      case_sensitive=case_sensitive):
                        processor = KeywordProcessor(case_sensitive=case_sensitive)
                        processor.add_keyword(keyword, replacement)
                        sentence = text + suffix
                        self.assertEqual(
                            processor.extract_keywords(sentence, span_info=True, max_cost=cost),
                            [(replacement, 0, len(text))],
                        )
                        self.assertEqual(
                            processor.replace_keywords(sentence, max_cost=cost), replacement + suffix
                        )
                        self.assertEqual(processor.extract_keywords(sentence, max_cost=cost - 1), [])
                        self.assertEqual(processor.replace_keywords(sentence, max_cost=cost - 1), sentence)

    def test_current_node_candidate_cost_and_depth(self):
        processor = KeywordProcessor()
        processor.add_keyword('cat')
        node = processor.keyword_trie_dict['c']['a']['t']
        self.assertEqual(list(processor.levensthein('xy', max_cost=2, start_node=node)),
                         [(node, 2, 0)])
        self.assertEqual(list(processor.levensthein('xy', max_cost=1, start_node=node)), [])

    def test_preserve_descendant_match_priority(self):
        for case_sensitive in (False, True):
            for tail in ('', ' dog'):
                for budget in (1, 2):
                    with self.subTest(case_sensitive=case_sensitive, tail=tail, budget=budget):
                        processor = KeywordProcessor(case_sensitive=case_sensitive)
                        processor.add_keyword('cat' + tail, 'CAT')
                        processor.add_keyword('cater' + tail, 'CATER')
                        sentence = 'catxr' + tail
                        self.assertEqual(
                            processor.extract_keywords(sentence, span_info=True, max_cost=budget),
                            [('CATER', 0, len(sentence))],
                        )
                        self.assertEqual(processor.replace_keywords(sentence, max_cost=budget), 'CATER')

from flashtext import KeywordProcessor
import unittest


class TestFuzzyBoundaries(unittest.TestCase):
    def test_phrase_separators_follow_word_boundaries(self):
        for separator in (' ', '-', '/', ':', '.', ',', '\t', '\r', '\n'):
            for case_sensitive in (False, True):
                with self.subTest(separator=separator, case_sensitive=case_sensitive):
                    processor = KeywordProcessor(case_sensitive=case_sensitive)
                    processor.add_keyword('new' + separator + 'york', 'NY')
                    sentence = 'naw' + separator + 'york'
                    self.assertEqual(
                        processor.extract_keywords(sentence, span_info=True, max_cost=1),
                        [('NY', 0, len(sentence))],
                    )
                    self.assertEqual(processor.replace_keywords(sentence, max_cost=1), 'NY')
                    self.assertEqual(processor.extract_keywords(sentence, max_cost=0), [])

    def test_configured_word_characters_are_not_phrase_separators(self):
        for separator in ('.', ',', '-', '/'):
            with self.subTest(separator=separator):
                processor = KeywordProcessor()
                processor.add_non_word_boundary(separator)
                processor.add_keyword('new' + separator + 'york', 'NY')
                sentence = 'naw' + separator + 'york'
                self.assertEqual(processor.extract_keywords(sentence, max_cost=1), ['NY'])
                self.assertEqual(processor.replace_keywords(sentence, max_cost=1), 'NY')

    def test_removed_word_characters_are_phrase_separators(self):
        processor = KeywordProcessor()
        processor.set_non_word_boundaries(processor.non_word_boundaries - {'_'})
        processor.add_keyword('new_york', 'NY')
        self.assertEqual(processor.extract_keywords('naw_york', max_cost=1), ['NY'])
        self.assertEqual(processor.replace_keywords('naw_york', max_cost=1), 'NY')

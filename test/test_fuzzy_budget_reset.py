from flashtext import KeywordProcessor
import unittest


class TestFuzzyBudgetReset(unittest.TestCase):
    cases = [
        ('naw zoo cot', 1, [('ANIMAL', 8, 11)], 'naw zoo ANIMAL'),
        ('naw/zoo cot', 1, [('ANIMAL', 8, 11)], 'naw/zoo ANIMAL'),
        ('naw! cot', 1, [('ANIMAL', 5, 8)], 'naw! ANIMAL'),
        ('naw yark cot', 1, [('ANIMAL', 9, 12)], 'naw yark ANIMAL'),
        ('nxx zoo cuut', 2, [('ANIMAL', 8, 12)], 'nxx zoo ANIMAL'),
        ('naw zoo cuut', 2, [('ANIMAL', 8, 12)], 'naw zoo ANIMAL'),
        ('naw zoo cot cot', 1, [('ANIMAL', 8, 11), ('ANIMAL', 12, 15)],
         'naw zoo ANIMAL ANIMAL'),
        ('naw york cot', 1, [('CITY', 0, 8), ('ANIMAL', 9, 12)],
         'CITY ANIMAL'),
        ('naw yark', 1, [], 'naw yark'),
        ('naw yark', 2, [('CITY', 0, 8)], 'CITY'),
        ('naw zoo cot', 0, [], 'naw zoo cot'),
        ('new york cat', 0, [('CITY', 0, 8), ('ANIMAL', 9, 12)],
         'CITY ANIMAL'),
        ('naw zoo cat', 1, [('ANIMAL', 8, 11)], 'naw zoo ANIMAL'),
    ]

    def processor(self, case_sensitive):
        processor = KeywordProcessor(case_sensitive=case_sensitive)
        processor.add_keyword('new york', 'CITY')
        processor.add_keyword('cat', 'ANIMAL')
        return processor

    def test_extract_budget_resets_after_failed_phrase(self):
        for case_sensitive in (False, True):
            processor = self.processor(case_sensitive)
            for sentence, budget, expected, _ in self.cases:
                with self.subTest(sentence=sentence, budget=budget,
                                  case_sensitive=case_sensitive):
                    self.assertEqual(processor.extract_keywords(
                        sentence, span_info=True, max_cost=budget), expected)

    def test_replace_budget_resets_after_failed_phrase(self):
        for case_sensitive in (False, True):
            processor = self.processor(case_sensitive)
            for sentence, budget, _, expected in self.cases:
                with self.subTest(sentence=sentence, budget=budget,
                                  case_sensitive=case_sensitive):
                    self.assertEqual(processor.replace_keywords(
                        sentence, max_cost=budget), expected)

    def test_case_insensitive_failed_prefix_keeps_original_text(self):
        processor = self.processor(False)
        sentence = 'NAW/ZOO CoT'
        self.assertEqual(processor.extract_keywords(
            sentence, span_info=True, max_cost=1), [('ANIMAL', 8, 11)])
        self.assertEqual(processor.replace_keywords(sentence, max_cost=1),
                         'NAW/ZOO ANIMAL')

from collections import defaultdict
from flashtext import KeywordProcessor
import logging
import unittest
import json
import re
import sys

logger = logging.getLogger(__name__)


class TestKPGetAllKeywords(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")

    def tearDown(self):
        logger.info("Ending.")

    def test_get_all_keywords(self):
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keyword('j2ee', 'Java')
        keyword_processor.add_keyword('colour', 'color')
        keyword_processor.get_all_keywords()
        self.assertEqual(keyword_processor.get_all_keywords(),
                         {'colour': 'color', 'j2ee': 'Java'},
                         "get_all_keywords didn't match expected results.")

    def test_get_all_keywords_beyond_recursion_limit(self):
        for case_sensitive in (False, True):
            with self.subTest(case_sensitive=case_sensitive):
                processor = KeywordProcessor(case_sensitive=case_sensitive)
                keyword = 'A' * (sys.getrecursionlimit() + 50)
                processor.add_keyword(keyword + 'B', 'longer')
                processor.add_keyword(keyword, 'long')
                processor.add_keyword('short', 'short')
                stored = keyword if case_sensitive else keyword.lower()
                suffix = 'B' if case_sensitive else 'b'

                self.assertEqual(processor.get_all_keywords(), {
                    stored + suffix: 'longer', stored: 'long', 'short': 'short',
                })
                self.assertEqual(len(processor), 3)
                self.assertEqual(processor.get_keyword(keyword), 'long')
                self.assertEqual(processor.extract_keywords(keyword), ['long'])

    def test_get_all_keywords_deep_subtree(self):
        processor = KeywordProcessor(case_sensitive=True)
        keyword = 'A' * (sys.getrecursionlimit() + 50)
        processor.add_keyword(keyword, 'long')

        self.assertEqual(processor.get_all_keywords(
            term_so_far='A', current_dict=processor.keyword_trie_dict['A']),
            {keyword: 'long'})

    def test_get_all_keywords_preserves_traversal_order(self):
        processor = KeywordProcessor()
        for keyword in ('cats', 'cat', 'car', 'dog'):
            processor.add_keyword(keyword)

        def expected_order(node, prefix=''):
            result = []
            for key in node:
                if key == '_keyword_':
                    result.append(prefix)
                else:
                    result.extend(expected_order(node[key], prefix + key))
            return result

        self.assertEqual(list(processor.get_all_keywords()),
                         expected_order(processor.keyword_trie_dict))
        self.assertEqual(processor.get_all_keywords(None, {}), {})


if __name__ == '__main__':
    unittest.main()

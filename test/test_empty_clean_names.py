import pytest

from flashtext import KeywordProcessor


@pytest.mark.parametrize('case_sensitive', [False, True])
def test_empty_clean_name_is_stored_and_can_be_removed(case_sensitive):
    processor = KeywordProcessor(case_sensitive=case_sensitive)
    assert processor.add_keyword('remove', '')
    assert processor.get_keyword('remove') == ''
    assert 'remove' in processor
    assert len(processor) == 1
    assert processor.remove_keyword('remove')
    assert 'remove' not in processor


@pytest.mark.parametrize('case_sensitive', [False, True])
def test_empty_clean_names_keep_extraction_spans(case_sensitive):
    processor = KeywordProcessor(case_sensitive=case_sensitive)
    processor.add_keyword('remove', '')
    assert processor.extract_keywords('prefix remove suffix', span_info=True) == [('', 7, 13)]
    assert processor.extract_keywords('remove') == ['']


@pytest.mark.parametrize('case_sensitive', [False, True])
def test_empty_clean_names_delete_keywords_without_losing_spaces(case_sensitive):
    processor = KeywordProcessor(case_sensitive=case_sensitive)
    processor.add_keyword('remove', '')
    assert processor.replace_keywords('remove and keep remove') == ' and keep '


def test_empty_longest_match_wins_over_nonempty_prefix():
    processor = KeywordProcessor()
    processor.add_keyword('new', 'N')
    processor.add_keyword('new york', '')
    assert processor.replace_keywords('new york city') == ' city'
    assert processor.extract_keywords('new york city') == ['']


def test_fuzzy_match_can_have_empty_clean_name():
    processor = KeywordProcessor()
    processor.add_keyword('apple', '')
    assert processor.replace_keywords('aple and pear', max_cost=1) == ' and pear'

import os
import string
import io
import nltk

class KeywordProcessor(object):
    """KeywordProcessor

    Attributes:
        _keyword (str): Used as key to store keywords in trie dictionary.
            Defaults to '_keyword_'
        non_word_boundaries (set(str)):
            Characters that will determine if the word is continuing.
            Defaults to set([A-Za-z0-9_])
        keyword_trie_dict (dict):
            Trie dict built character by character, that is used for lookup
            Defaults to empty dictionary
        case_sensitive (boolean):
            if the search algorithm should be case sensitive or not.
            Defaults to False

    Examples:
        >>> # import module
        >>> from flashtext import KeywordProcessor
        >>> # Create an object of KeywordProcessor
        >>> keyword_processor = KeywordProcessor()
        >>> # add keywords
        >>> keyword_names = ['NY', 'new-york', 'SF']
        >>> clean_names = ['new york', 'new york', 'san francisco']
        >>> for keyword_name, clean_name in zip(keyword_names, clean_names):
        >>>     keyword_processor.add_keyword(keyword_name, clean_name)
        >>> keywords_found = keyword_processor.extract_keywords('I \
                            love SF and NY. new-york is the best.')
        >>> keywords_found
        >>> ['san francisco', 'new york', 'new york']

    Note:
        * loosely based on `Aho-Corasick algorithm
        <https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm>`_.
        * Idea came from this `Stack Overflow Question
        <https://stackoverflow.com/questions/44178449/regex-replace-is-\
        taking-time-for-millions-of-documents-how-to-make-it-faster>`_.
    """

    def __init__(self, case_sensitive=False):
        """
        Args:
            case_sensitive (boolean):
                Keyword search should be case sensitive set or not.
                Defaults to False
        """
        self._keyword = '_keyword_'
        self._white_space_chars = set(['.', '\t', '\n', '\a', ' ', ','])
        try:
            # python 2.x
            self.non_word_boundaries = set(string.digits +
                                           string.letters + '_')
        except AttributeError:
            # python 3.x
            self.non_word_boundaries = set(string.digits +
                                           string.ascii_letters + '_')
        self.keyword_trie_dict = dict()
        self.case_sensitive = case_sensitive
        self._terms_in_trie = 0

    def __len__(self):
        """Number of terms present in the keyword_trie_dict

        Returns:
            length : int
                Count of number of distinct terms in trie dictionary.

        """
        return self._terms_in_trie

    def __contains__(self, word):
        """To check if word is present in the keyword_trie_dict

        Args:
            word : string
                word that you want to check

        Returns:
            status : bool
                If word is present as it is in keyword_trie_dict
                then we return True, else False

        Examples:
            >>> keyword_processor.add_keyword('Big Apple')
            >>> 'Big Apple' in keyword_processor
            >>> # True

        """
        if not self.case_sensitive:
            word = word.lower()
        curr_dict = self.keyword_trie_dict
        len_covered = 0
        for char in word:
            if char in curr_dict:
                curr_dict = curr_dict[char]
                len_covered += 1
            else:
                break
        return self._keyword in curr_dict and len_covered == len(word)

    def __getitem__(self, word):
        """if word is present in keyword_trie_dict return the clean name for it.

        Args:
            word : string
                word that you want to check

        Returns:
            keyword : string
                If word is present as it is in keyword_trie_dict
                then we return keyword mapped to it.

        Examples:
            >>> keyword_processor.add_keyword('Big Apple', 'New York')
            >>> keyword_processor['Big Apple']
            >>> # New York
        """
        if not self.case_sensitive:
            word = word.lower()
        curr_dict = self.keyword_trie_dict
        len_covered = 0
        for char in word:
            if char in curr_dict:
                curr_dict = curr_dict[char]
                len_covered += 1
            else:
                break
        if self._keyword in curr_dict and len_covered == len(word):
            return curr_dict[self._keyword]

    def __setitem__(self, keyword, clean_name=None):
        """To add keyword to the dictionary
        pass the keyword and the clean name it maps to.

        Args:
            keyword : string
                keyword that you want to identify

            clean_name : string
                clean term for that keyword that you would want
                to get back in return or replace
                if not provided, keyword will be used as the clean name also.

        Examples:
            >>> keyword_processor['Big Apple'] = 'New York'
        """
        status = False
        if not clean_name and keyword:
            clean_name = keyword

        if keyword and clean_name:
            if not self.case_sensitive:
                keyword = keyword.lower()
            curr_dict = self.keyword_trie_dict
            for letter in keyword:
                curr_dict = curr_dict.setdefault(letter, {})
            if self._keyword not in curr_dict:
                status = True
                self._terms_in_trie += 1
            curr_dict[self._keyword] = clean_name
        return status

    def __delitem__(self, keyword):
        """To remove keyword from the dictionary
        pass the keyword and the clean name it maps to.

        Args:
            keyword : string
                keyword that you want to remove if it's present

        Examples:
            >>> keyword_processor.add_keyword('Big Apple')
            >>> del keyword_processor['Big Apple']
        """
        status = False
        if keyword:
            if not self.case_sensitive:
                keyword = keyword.lower()
            curr_dict = self.keyword_trie_dict
            character_trie_list = []
            for letter in keyword:
                if letter in curr_dict:
                    character_trie_list.append((letter, curr_dict))
                    curr_dict = curr_dict[letter]
                else:
                    # if character is not found, break out of the loop
                    curr_dict = None
                    break
            # remove the characters from trie dict if there
            # are no other keywords with them
            if curr_dict and self._keyword in curr_dict:
                # we found a complete match for input keyword.
                character_trie_list.append((self._keyword, curr_dict))
                character_trie_list.reverse()

                for key_to_remove, dict_pointer in character_trie_list:
                    if len(dict_pointer.keys()) == 1:
                        dict_pointer.pop(key_to_remove)
                    else:
                        # more than one key means more than 1 path.
                        # Delete not required path and keep the other
                        dict_pointer.pop(key_to_remove)
                        break
                # successfully removed keyword
                status = True
                self._terms_in_trie -= 1
        return status

    def __iter__(self):
        """Disabled iteration as get_all_keywords() is the right way to iterate
        """
        raise NotImplementedError("Please use get_all_keywords() instead")

    def set_non_word_boundaries(self, non_word_boundaries):
        """set of characters that will be considered as part of word.

        Args:
            non_word_boundaries (set(str)):
                Set of characters that will be considered as part of word.

        """
        self.non_word_boundaries = non_word_boundaries

    def add_non_word_boundary(self, character):
        """add a character that will be considered as part of word.

        Args:
            character (char):
                Character that will be considered as part of word.

        """
        self.non_word_boundaries.add(character)

    def add_keyword(self, keyword, clean_name=None):
        """To add one or more keywords to the dictionary
        pass the keyword and the clean name it maps to.

        Args:
            keyword : string
                keyword that you want to identify

            clean_name : string
                clean term for that keyword that you would want
                to get back in return or replace
                if not provided, keyword will be used as the clean name also.

        Returns:
            status : bool
                The return value. True for success, False otherwise.

        Examples:
            >>> keyword_processor.add_keyword('Big Apple', 'New York')
            >>> # This case 'Big Apple' will return 'New York'
            >>> # OR
            >>> keyword_processor.add_keyword('Big Apple')
            >>> # This case 'Big Apple' will return 'Big Apple'
        """
        return self.__setitem__(keyword, clean_name)

    def remove_keyword(self, keyword):
        """To remove one or more keywords from the dictionary
        pass the keyword and the clean name it maps to.

        Args:
            keyword : string
                keyword that you want to remove if it's present

        Returns:
            status : bool
                The return value. True for success, False otherwise.

        Examples:
            >>> keyword_processor.add_keyword('Big Apple')
            >>> keyword_processor.remove_keyword('Big Apple')
            >>> # Returns True
            >>> # This case 'Big Apple' will no longer be a recognized keyword
            >>> keyword_processor.remove_keyword('Big Apple')
            >>> # Returns False

        """
        return self.__delitem__(keyword)

    def get_keyword(self, word):
        """if word is present in keyword_trie_dict return the clean name for it.

        Args:
            word : string
                word that you want to check

        Returns:
            keyword : string
                If word is present as it is in keyword_trie_dict
                then we return keyword mapped to it.

        Examples:
            >>> keyword_processor.add_keyword('Big Apple', 'New York')
            >>> keyword_processor.get('Big Apple')
            >>> # New York
        """
        return self.__getitem__(word)

    def add_keyword_from_file(self, keyword_file, encoding="utf-8"):
        """To add keywords from a file

        Args:
            keyword_file : path to keywords file
            encoding : specify the encoding of the file

        Examples:
            keywords file format can be like:

            >>> # Option 1: keywords.txt content
            >>> # java_2e=>java
            >>> # java programing=>java
            >>> # product management=>product management
            >>> # product management techniques=>product management

            >>> # Option 2: keywords.txt content
            >>> # java
            >>> # python
            >>> # c++

            >>> keyword_processor.add_keyword_from_file('keywords.txt')

        Raises:
            IOError: If `keyword_file` path is not valid

        """
        if not os.path.isfile(keyword_file):
            raise IOError("Invalid file path {}".format(keyword_file))
        with io.open(keyword_file, encoding=encoding) as f:
            for line in f:
                if '=>' in line:
                    keyword, clean_name = line.split('=>')
                    self.add_keyword(keyword, clean_name.strip())
                else:
                    keyword = line.strip()
                    self.add_keyword(keyword)

    def add_keywords_from_dict(self, keyword_dict):
        """To add keywords from a dictionary

        Args:
            keyword_dict (dict):
            A dictionary with `str` key and(list `str`) as value

        Examples:
            >>> keyword_dict = {
                    "java": ["java_2e", "java programing"],
                    "product management": ["PM", "product manager"]
                }
            >>> keyword_processor.add_keywords_from_dict(keyword_dict)

        Raises:
            AttributeError: If value for a key in `keyword_dict` is not a list.

        """
        for clean_name, keywords in keyword_dict.items():
            if not isinstance(keywords, list):
                raise AttributeError("Value of key {}\
                    should be a list".format(clean_name))

            for keyword in keywords:
                self.add_keyword(keyword, clean_name)

    def remove_keywords_from_dict(self, keyword_dict):
        """To remove keywords from a dictionary

        Args:
            keyword_dict (dict):
            A dictionary with `str` key and(list `str`) as value

        Examples:
            >>> keyword_dict = {
                    "java": ["java_2e", "java programing"],
                    "product management": ["PM", "product manager"]
                }
            >>> keyword_processor.remove_keywords_from_dict(keyword_dict)

        Raises:
            AttributeError: If value for a key in `keyword_dict` is not a list.

        """
        for clean_name, keywords in keyword_dict.items():
            if not isinstance(keywords, list):
                raise AttributeError("Value of key {} should\
                    be a list".format(clean_name))

            for keyword in keywords:
                self.remove_keyword(keyword)

    def add_keywords_from_list(self, keyword_list):
        """To add keywords from a list

        Args:
            keyword_list (list(str)): List of keywords to add

        Examples:
            >>> keyword_processor.add_keywords_from_list(["java", "python"]})
        Raises:
            AttributeError: If `keyword_list` is not a list.

        """
        if not isinstance(keyword_list, list):
            raise AttributeError("keyword_list should be a list")

        for keyword in keyword_list:
            self.add_keyword(keyword)

    def remove_keywords_from_list(self, keyword_list):
        """To remove keywords present in list

        Args:
            keyword_list (list(str)): List of keywords to remove

        Examples:
        >>> keyword_processor.remove_keywords_from_list(["java", "python"]})
        Raises:
            AttributeError: If `keyword_list` is not a list.

        """
        if not isinstance(keyword_list, list):
                raise AttributeError("keyword_list should be a list")

        for keyword in keyword_list:
            self.remove_keyword(keyword)

    def get_all_keywords(self, term_so_far='', curr_dict=None):
        """Recursively builds a dictionary of keywords present in the dictionary
        And the clean name mapped to those keywords.

        Args:
            term_so_far : string
                term built so far by adding all previous characters
            curr_dict : dict
                current recursive position in dictionary

        Returns:
            terms_present : dict
                A map of key and value where each key is a term
                in the keyword_trie_dict.
                And value mapped to it is the clean name mapped to it.

        Examples:
            >>> keyword_processor = KeywordProcessor()
            >>> keyword_processor.add_keyword('j2ee', 'Java')
            >>> keyword_processor.add_keyword('Python', 'Python')
            >>> keyword_processor.get_all_keywords()
            >>> {'j2ee': 'Java', 'python': 'Python'}
            >>> # NOTE: for case_insensitive all keys will be lowercased.
        """
        terms_present = {}
        if not term_so_far:
            term_so_far = ''
        if curr_dict is None:
            curr_dict = self.keyword_trie_dict
        for key in curr_dict:
            if key == '_keyword_':
                terms_present[term_so_far] = curr_dict[key]
            else:
                sub_values = self.get_all_keywords(term_so_far +
                                                   key, curr_dict[key])
                for key in sub_values:
                    terms_present[key] = sub_values[key]
        return terms_present

    def extract_keywords(self, sentence, span_info=False, fetch_sent=False):
        """Searches in the string for all keywords present in corpus.
        Keywords present are added to a list `keywords_extracted` and returned.

        Args:
            sentence (str): Line of text where we will search for keywords

        Returns:
            keywords_extracted (list(str)):
            List of terms/keywords found in sentence that match our corpus

        Examples:
            >>> from flashtext import KeywordProcessor
            >>> keyword_processor = KeywordProcessor()
            >>> keyword_processor.add_keyword('Big Apple', 'New York')
            >>> keyword_processor.add_keyword('Bay Area')
            >>> keywords_found = keyword_processor.extract_keywords('I\
                                 love Big Apple and Bay Area.')
            >>> keywords_found
            >>> ['New York', 'Bay Area']

        """
        keywords_extracted = []
        if not sentence:
            # if sentence is empty or none just return empty list
            return keywords_extracted
        if not self.case_sensitive:
            sentence = sentence.lower()
        idx = 0
        sentences_with_keyword = []

        def _helper(sentence, idx):
            reset_curr_dict = False
            seq_start_pos = seq_end_pos = idx
            sentence_len = len(sentence)
            curr_dict = self.keyword_trie_dict
            while idx < sentence_len:
                char = sentence[idx]
                # print(char)
                # when we reach a character that might denote word end
                if char not in self.non_word_boundaries:

                    # if end is present in curr_dict
                    if self._keyword in curr_dict or char in curr_dict:
                        # update longest sequence found
                        seq_found = None
                        longest_seq_found = None
                        is_longer_seq_found = False
                        if self._keyword in curr_dict:
                            seq_found = curr_dict[self._keyword]
                            longest_seq_found = curr_dict[self._keyword]
                            seq_end_pos = idx

                        # re look for longest_sequence from this position
                        if char in curr_dict:
                            curr_dict_continued = curr_dict[char]

                            idy = idx + 1
                            while idy < sentence_len:
                                inner_char = sentence[idy]
                                if inner_char not in self.non_word_boundaries\
                                   and self._keyword in curr_dict_continued:
                                    # update longest sequence found
                                    longest_seq_found = curr_dict_continued[
                                                        self._keyword]
                                    seq_end_pos = idy
                                    is_longer_seq_found = True
                                    print("sentence longer")
                                if inner_char in curr_dict_continued:
                                    curr_dict_continued = curr_dict_continued[
                                                          inner_char]
                                else:
                                    break
                                idy += 1
                            else:
                                # end of sentence reached.
                                if self._keyword in curr_dict_continued:
                                    # update longest sequence found
                                    longest_seq_found = curr_dict_continued[
                                                        self._keyword]
                                    seq_end_pos = idy
                                    is_longer_seq_found = True
                            if is_longer_seq_found:
                                idx = seq_end_pos
                        curr_dict = self.keyword_trie_dict
                        if longest_seq_found:
                            keywords_extracted.append((longest_seq_found,
                                                       seq_start_pos, idx))
                            if fetch_sent:
                                # print("longest_seq_found: ", sentence)
                                sentences_with_keyword.append(sentence)
                        reset_curr_dict = True
                    else:
                        # we reset curr_dict
                        curr_dict = self.keyword_trie_dict
                        reset_curr_dict = True
                elif char in curr_dict:
                    # we can continue from this char
                    curr_dict = curr_dict[char]
                else:
                    # we reset curr_dict
                    curr_dict = self.keyword_trie_dict
                    reset_curr_dict = True
                    # skip to end of word
                    idy = idx + 1
                    while idy < sentence_len:
                        char = sentence[idy]
                        if char not in self.non_word_boundaries:
                            break
                        idy += 1
                    idx = idy
                # if we are end of sentence and have a sequence discovered
                if idx + 1 >= sentence_len:
                    if self._keyword in curr_dict:
                        seq_found = curr_dict[self._keyword]
                        keywords_extracted.append((seq_found, seq_start_pos,
                                                   sentence_len))
                idx += 1
                if reset_curr_dict:
                    reset_curr_dict = False
                    seq_start_pos = idx
        if fetch_sent:
            sentences = nltk.sent_tokenize(sentence)  # sentence is paragraph
            for each_sentence in sentences:
                idx = 0
                _helper(each_sentence, idx)
            return sentences_with_keyword
        else:
            _helper(sentence, idx)
            if span_info:
                return keywords_extracted
            return [value[0] for value in keywords_extracted]

    def replace_keywords(self, sentence):
        """Searches in the string for all keywords present in corpus.
        Keywords present are replaced by the clean name and
        a new string is returned.

        Args:
            sentence (str): Line of text where we will replace keywords

        Returns:
            new_sentence (str): Line of text with replaced keywords

        Examples:
            >>> from flashtext import KeywordProcessor
            >>> keyword_processor = KeywordProcessor()
            >>> keyword_processor.add_keyword('Big Apple', 'New York')
            >>> keyword_processor.add_keyword('Bay Area')
            >>> new_sentence = keyword_processor.replace_keywords('I
                                love Big Apple and bay area.')
            >>> new_sentence
            >>> 'I love New York and Bay Area.'

        """
        if not sentence:
            # if sentence is empty or none just return the same.
            return sentence
        new_sentence = []
        orig_sentence = sentence
        if not self.case_sensitive:
            sentence = sentence.lower()
        curr_word = ''
        curr_dict = self.keyword_trie_dict
        curr_white_space = ''
        seq_end_pos = 0
        idx = 0
        sentence_len = len(sentence)
        while idx < sentence_len:
            char = sentence[idx]
            curr_word += orig_sentence[idx]
            # when we reach whitespace
            if char not in self.non_word_boundaries:
                curr_white_space = char
                # if end is present in curr_dict
                if self._keyword in curr_dict or char in curr_dict:
                    # update longest sequence found
                    seq_found = None
                    longest_seq_found = None
                    is_longer_seq_found = False
                    if self._keyword in curr_dict:
                        seq_found = curr_dict[self._keyword]
                        longest_seq_found = curr_dict[self._keyword]
                        seq_end_pos = idx

                    # re look for longest_sequence from this position
                    if char in curr_dict:
                        curr_dict_continued = curr_dict[char]
                        curr_word_continued = curr_word
                        idy = idx + 1
                        while idy < sentence_len:
                            inner_char = sentence[idy]
                            curr_word_continued += orig_sentence[idy]
                            if inner_char not in self.non_word_boundaries \
                            and self._keyword in curr_dict_continued:
                                # update longest sequence found
                                curr_white_space = inner_char
                                longest_seq_found = curr_dict_continued[
                                                    self._keyword]
                                seq_end_pos = idy
                                is_longer_seq_found = True
                            if inner_char in curr_dict_continued:
                                curr_dict_continued = curr_dict_continued[
                                                      inner_char]
                            else:
                                break
                            idy += 1
                        else:
                            # end of sentence reached.
                            if self._keyword in curr_dict_continued:
                                # update longest sequence found
                                curr_white_space = ''
                                longest_seq_found = curr_dict_continued[
                                                    self._keyword]
                                seq_end_pos = idy
                                is_longer_seq_found = True
                        if is_longer_seq_found:
                            idx = seq_end_pos
                            curr_word = curr_word_continued
                    curr_dict = self.keyword_trie_dict
                    if longest_seq_found:
                        new_sentence.append(longest_seq_found +
                                            curr_white_space)
                        curr_word = ''
                        curr_white_space = ''
                    else:
                        new_sentence.append(curr_word)
                        curr_word = ''
                        curr_white_space = ''
                else:
                    # we reset curr_dict
                    curr_dict = self.keyword_trie_dict
                    new_sentence.append(curr_word)
                    curr_word = ''
                    curr_white_space = ''
            elif char in curr_dict:
                # we can continue from this char
                curr_dict = curr_dict[char]
            else:
                # we reset curr_dict
                curr_dict = self.keyword_trie_dict
                # skip to end of word
                idy = idx + 1
                while idy < sentence_len:
                    char = sentence[idy]
                    curr_word += orig_sentence[idy]
                    if char not in self.non_word_boundaries:
                        break
                    idy += 1
                idx = idy
                new_sentence.append(curr_word)
                curr_word = ''
                curr_white_space = ''
            # if we are end of sentence and have a sequence discovered
            if idx + 1 >= sentence_len:
                if self._keyword in curr_dict:
                    seq_found = curr_dict[self._keyword]
                    new_sentence.append(seq_found)
                else:
                    new_sentence.append(curr_word)
            idx += 1
        return "".join(new_sentence)

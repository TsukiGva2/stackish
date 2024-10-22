import re

from .configuration import (
    DELIM_QUOTE_END,
    INDEX_QUOTE_BEGIN,
    INDEX_QUOTE_END,
    INDEX_SQUOTE_BEGIN,
)
from .errors import Forth_CompilationError


class Tokenizer:
    def __init__(self):
        self.words = iter([])
        self.skip = False
        self.match_word = re.compile(
            r"[?/A-Za-z!@#$%&*()\[\]^~'`\"\\+=-_.,><{}][?/A-Za-z0-9!@#$%&*()\[\]^~'`\"\\+=-_.,><{}]*"
        )

    # utils
    def next(self):
        try:
            return next(self.words)
        except StopIteration:
            raise EOFError("Unexpected EOF.")  # TODO

    def word(self, w):
        if self.match_word.match(w):
            return w
        raise Forth_CompilationError(f"Invalid identifier '{w}")

    # makers
    def quote(self, word):
        w = word[INDEX_QUOTE_BEGIN:]

        if w.endswith(DELIM_QUOTE_END):
            return w[:INDEX_QUOTE_END]

        quote = [w]

        while not (w := self.next()).endswith(DELIM_QUOTE_END):
            quote.append(w)

        quote.append(w[:INDEX_QUOTE_END])

        result = " ".join(quote)

        return result

    def simple_quote(self, word):
        return word[INDEX_SQUOTE_BEGIN:]

    def symbol(self, word):
        w = self.word(word)

        return w

    def number(self, num):
        n = float(num)
        return n

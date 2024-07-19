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
            r"[?/A-Za-z!@#$%&*()\[\]^~'`\"\\+=-_.,><{}:;][?/A-Za-z0-9!@#$%&*()\[\]^~'`\"\\+=-_.,><{}:;]*"
        )

    # utils
    def next(self, caller):
        try:
            return next(self.words)
        except StopIteration:
            raise EOFError(f"Unexpected EOF in definition for '{caller}'.")  # TODO

    def isword(self, w):
        if self.match_word.match(w):
            return w

        raise Forth_CompilationError(f"Invalid identifier '{w}'")

    # makers
    def quote(self, word):
        w = word[INDEX_QUOTE_BEGIN:]

        if w.endswith(DELIM_QUOTE_END):
            return w[:INDEX_QUOTE_END]

        quote = [w]

        while not (w := self.next("Quote")).endswith(DELIM_QUOTE_END):
            quote.append(w)

        quote.append(w[:INDEX_QUOTE_END])

        result = " ".join(quote)

        return result

    def simple_quote(self, word):
        return word[INDEX_SQUOTE_BEGIN:]

    def number(self, num):
        n = float(num)  # TODO @DESIGN @OPTIMIZATION: separate int/float types
        return n

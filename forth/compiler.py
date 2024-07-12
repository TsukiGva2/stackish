import re

from .configuration import (
    COMPILE,
    DELIM_COLON_BEGIN,
    DELIM_COLON_END,
    DELIM_QUOTE_BEGIN,
    DELIM_QUOTE_END,
    DELIM_SQUOTE_BEGIN,
    INDEX_QUOTE_BEGIN,
    INDEX_QUOTE_END,
    INDEX_SQUOTE_BEGIN,
    INTERPRET,
)
from .errors import Forth_CompilationError
from .instruction import Instruction


class Compiler:
    def __init__(self):
        self.symbols = set()
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

    # operations
    @staticmethod
    def push(n):
        return Instruction(lambda state: state.push(n), name=f"PUSH {n}")

    @staticmethod
    def drop():
        return Instruction(lambda state: state.drop(), name="DROP")

    @staticmethod
    def dup():
        return Instruction(lambda state: state.dup(), name="DUP")

    def colon(self):
        word = self.word(self.next())
        return Instruction(
            lambda state: state.switch(COMPILE),
            lambda state: state.header(word),
            name=f"FUNC {word}",
            compiled=False,
        )

    def endcolon(self):
        return Instruction(
            lambda state: state.switch(INTERPRET),
            lambda state: state.close_header(),
            name="END",
            compiled=False,
        )

    def find(self, word):
        return Instruction(
            lambda state: state.fetch(word), name=f"FIND {word}", skippable=False
        )

    # makers
    def quote(self, word):
        w = word[INDEX_QUOTE_BEGIN:]

        if w.endswith(DELIM_QUOTE_END):
            return self.push(w[:INDEX_QUOTE_END])

        quote = [w]

        while not (w := self.next()).endswith(DELIM_QUOTE_END):
            quote.append(w)

        quote.append(w[:INDEX_QUOTE_END])

        result = " ".join(quote)
        return self.push(result)

    def simple_quote(self, word):
        return self.push(word[INDEX_SQUOTE_BEGIN:])

    def symbol(self, word):
        w = self.word(word)

        return self.find(w)

    def number(self, num):
        n = float(num)
        return self.push(n)

    def compile(self, words):
        self.words = iter(words)

        for w in self.words:
            meaning = ...

            if w.startswith(DELIM_QUOTE_BEGIN):
                yield self.quote(w)
                continue

            if w.startswith(DELIM_SQUOTE_BEGIN):
                yield self.simple_quote(w)
                continue

            if w == DELIM_COLON_BEGIN:
                yield self.colon()
                continue

            if w == DELIM_COLON_END:
                yield self.endcolon()
                continue

            try:
                meaning = self.number(w)
            except ValueError:
                meaning = self.symbol(w)

            yield meaning

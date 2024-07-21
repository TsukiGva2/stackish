from .compiler_error import Forth_CompilationError
from .configuration import DELIM_QUOTE_BEGIN, DELIM_SQUOTE_BEGIN
from .std.builtin import BuiltinFunctions
from .tokenizer import Tokenizer


class Compiler(Tokenizer):
    def __init__(self):
        Tokenizer.__init__(self)
        self.symbols = set()

    def create(self):
        return BuiltinFunctions.create(self)

    def literal(self, value):
        return BuiltinFunctions.literal(value)

    def word(self, word):
        return BuiltinFunctions.word(word)

    def compile(self, words):
        self.words = iter(words.split())

        for w in self.words:
            if w.startswith(DELIM_QUOTE_BEGIN):
                yield self.literal(self.quote(w))
                continue

            if w.startswith(DELIM_SQUOTE_BEGIN):
                yield self.literal(self.simple_quote(w))
                continue

            try:
                yield self.literal(self.number(w))
                continue
            except ValueError:
                yield self.word(self.isword(w))
                continue

            raise Forth_CompilationError

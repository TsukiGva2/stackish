from .configuration import DELIM_QUOTE_BEGIN, DELIM_SQUOTE_BEGIN
from .errors import Forth_CompilationError
from .instruction import Instruction
from .std import StdFunctions
from .tokenizer import Tokenizer


class Compiler(Tokenizer):
    def __init__(self):
        Tokenizer.__init__(self)
        self.symbols = set()

    def find(self, word):
        return Instruction(
            lambda state: state.find(word), skippable=False, compiled=False, name="find"
        )

    def create(self):
        w = self.next()
        return Instruction(lambda state: state.header_set_word(w))

    def literal(self, value):
        return StdFunctions.literal(value)

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
                yield self.find(self.symbol(w))
                continue

            raise Forth_CompilationError

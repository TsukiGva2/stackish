from .configuration import DELIM_QUOTE_BEGIN, DELIM_SQUOTE_BEGIN
from .errors import Forth_CompilationError
from .instruction import Instruction
from .tokenizer import Tokenizer


class Compiler(Tokenizer):
    def __init__(self):
        Tokenizer.__init__(self)
        self.symbols = set()

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

    def find(self, word):
        return Instruction(
            lambda state: state.fetch(word),
            name=f"FIND {word}",
            skippable=False,
            compiled=False,
        )

    def literal(self, value):
        return self.push(value)

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

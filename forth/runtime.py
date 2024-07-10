from collections import deque

from .configuration import INTERPRET
from .errors import Forth_EvaluationError
from .wordtable import WordTable


class Runtime:
    def __init__(self):
        self.stack = deque([])
        self.state = INTERPRET
        self.words = WordTable()

    # operations
    def push(self, *args):
        self.stack.extend(args)

        return args

    def drop(self):
        self.stack.pop()

        return 0

    def dup(self):
        n = self.stack.pop()
        self.push(n, n)

        return n

    def header(self, w):
        return self.words.new(w)

    def close_header(self):
        return self.words.end()

    def fetch(self, w):
        instructions = self.words.find(w)
        self.exec(instructions)

        return w

    def insert(self, w):
        return self.words.insert(w)

    def switch(self, s):
        if self.state == s:
            raise Forth_EvaluationError("Unexpected state switch (double :/;)")

        self.state = s

        return s

    # functs
    def eval(self, instruction):
        return instruction.run(self)

    def exec(self, instructions):
        return [self.eval(i) for i in instructions]

from collections import deque

from stackish_command import Command

from .configuration import INTERPRET

# from .errors import Forth_EvaluationError
from .wordtable import WordTable


class Runtime:
    def __init__(self, shell=None):
        self.stack = deque([])
        self.state = INTERPRET
        self.words = WordTable()

    # operations
    def push(self, *args):
        self.stack.extend(args)

        return args

    def drop(self):
        return self.stack.pop()

    def dup(self):
        n = self.stack.pop()
        self.push(n, n)

        return n

    def swap(self):
        self.stack.rotate(1)
        return 1

    def header(self, w):
        return self.words.new(w)

    def close_header(self):
        return self.words.end()

    def fetch(self, w):
        instructions = self.words.find(w)

        try:
            self.eval(instructions)
        except AttributeError:
            self.exec(instructions)

        return w

    def insert(self, w):
        return self.words.insert(w)

    def switch(self, s):
        if self.state == s:
            # raise Forth_EvaluationError("Unexpected state switch (double :/;)")
            return

        self.state = s

        return s

    # IO
    def run_shell(self, command):
        # TODO @IMPROVEMENT: Generalize the function
        # TODO @WIP:
        #   Implement PIPE/FILE OUTPUT Logic
        c = Command(command)
        return c.execute()

    # functs
    def eval(self, instruction):
        return instruction.run(self)

    def exec(self, instructions):
        return [self.eval(i) for i in instructions]

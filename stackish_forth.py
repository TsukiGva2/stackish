from functools import partial
from queue import deque

# - ls
# . .. .git/ main.py
# - : working_dir pwd ;
# OK WORKING_DIR
# - .. working_dir ( pwd .. )
# /home/tortea
#

# TODO: the objective is a C implementation
# of this forth system

INTERPRET = 0
COMPILE = 1


class Forth_UnderflowError(IndexError): ...


class Runtime:
    def __init__(self):
        self.stack = deque([])
        self.state = INTERPRET
        self.words = {}


class Compiler:
    def __init__(self):
        self.symbols = set()

        self.skip = False

    # operations
    def push(self, n):
        return (lambda state: state.push(n),)

    def popn(self, count):
        return (lambda state: state.pop(count),)

    def dup(self):
        return (lambda state: state.dup(),)

    def colon(self):
        return (self.push(self.next()), lambda state: state.switch(COMPILE))

    # makers
    def symbol(self, word):
        self.symbols = 0

    def number(self, num):
        n = int(num)
        return self.compile_push(n)

    def compile(self, words):
        for w in words:
            if self.skip:
                self.skip = not self.skip
                continue

            meaning = ...

            try:
                meaning = self.number(w)
            except ValueError:
                meaning = self.symbol(w)

            yield meaning


class System:
    def __init__(self):
        self.state = Runtime()
        self.compiler = Compiler()

    def compile(self): ...
    def interpret(self): ...

    def do_string(self, line):
        if line == "":
            return "OK"

        line = line.split()

        compiled = self.compiler.compile(line)

        self.state.exec(compiled)

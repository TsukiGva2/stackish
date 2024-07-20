from collections import deque

from repl.command import Command

from .configuration import INTERPRET
from .errors import Forth_EvaluationError, Forth_NotImplemented
from .instruction import Instruction, Word, get_instruction_status
from .signal import ForthSignal
from .std.builtin import BuiltinFunctions
from .words import Words


# TODO NOTE @DESIGN
# My implementation is kind of very far away from the
# simplicity of NEXT, this is unintentional and a @WIP
# still looking into simplifying things!
class Runtime:
    def __init__(self, shell=None):
        self.stack = deque([])
        self.state = INTERPRET
        self.words = Words()

        self.expecting = None

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

    # TODO @IMPROVEMENT: Look for an implementation closer to DOCOL
    def find(self, word):
        entry = self.words.find(word)
        return entry

    def immediate_find(self, w):
        entry = self.words.find(w)

        entry.compilable = False  # run immediately
        self.eval(entry)

        return w

    # XXX: workaround for getting a word from compilation
    # stream
    def word(self):
        self.expecting = Word
        return "word"

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

    # evaluation

    def exit(self):
        return ForthSignal.EXIT

    def simple_eval(self, instruction):
        return instruction.run(self)

    def immediate(self):
        return self.words.header.set_flags(compiled=False)

    def new_word(self, w):
        return self.words.new_word(w)

    def expect(self, instruction):
        if not isinstance(instruction, self.expecting):
            raise Forth_EvaluationError(f"Unexpected value! expected {self.expecting}")

        if self.expecting == Word:
            self.expecting = None

            return self.simple_eval(BuiltinFunctions.literal(instruction.token))

        raise Forth_NotImplemented("Can't expect a non-word value")

    # TODO @WIP XXX @OVERSIGHT: this 'expected_type' logic reveals a
    # larger issue with this implementation, hinting that
    # possibly the compiler and runtime are not well integrated,
    # forcing it to emulate getting a WORD from 'input', for example
    def eval(self, instruction):
        if self.expecting is not None:
            return self.expect(instruction)

        # I'm cooked
        # FIXME @OVERSIGHT: How does this behave with EXIT?
        if isinstance(instruction, Word):
            return self.eval(self.find(instruction.token))

        if isinstance(instruction, Instruction):
            return instruction.run(self)

        raise Forth_EvaluationError(f"Undefined type: {type(instruction)}")

    def exec(self, instructions):
        evaluated = (self.eval(i) for i in instructions)

        results = [
            (report.name, get_instruction_status(report.status)) for report in evaluated
        ]

        return (self.stack, results, self.words.list())

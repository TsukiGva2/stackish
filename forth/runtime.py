from collections import deque

from repl.command import Command

from .configuration import INTERPRET
from .instruction import Instruction, Word, get_instruction_status
from .runtime_error import (
    Forth_Runtime_EvaluationError,
    Forth_Runtime_NotImplementedError,
    Forth_Runtime_UnderflowError,
    Forth_Runtime_UnexpectedEOFError,
)
from .signal import ForthSignal
from .std.builtin import BuiltinFunctions
from .words import ForthDict


# TODO NOTE @DESIGN
# My implementation is kind of very far away from the
# simplicity of NEXT, this is unintentional and a @WIP
# still looking into simplifying things!
class Runtime:
    def __init__(self, shell=None):
        self.stack = deque([])
        self.state = INTERPRET
        self.words = ForthDict()

        self.instructions = iter([])

    # operations
    def push(self, *args):
        self.stack.extend(args)

        return args

    def drop(self):
        try:
            return self.stack.pop()
        except IndexError:
            raise Forth_Runtime_UnderflowError("Stack underflow")

    def peek(self):
        try:
            return self.stack[-1]
        except IndexError:
            return "EMPTY"

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

    # TODO @WIP XXX @OVERSIGHT: this 'expected_type' logic reveals a
    # larger issue with this implementation, hinting that
    # possibly the compiler and runtime are not well integrated,
    # forcing it to emulate getting a WORD from 'input', for example
    def expect(self, instruction_type):
        try:
            instruction = next(self.instructions)
        except StopIteration:
            raise Forth_Runtime_UnexpectedEOFError(
                f"Unexpected EOF! expected {instruction_type}"
            )

        if not isinstance(instruction, instruction_type):
            raise Forth_Runtime_EvaluationError(
                f"Unexpected value! expected {self.expecting}"
            )

        if instruction_type == Word:
            return self.simple_eval(BuiltinFunctions.literal(instruction.token))

        raise Forth_Runtime_NotImplementedError("Can't expect a non-word value")

    # XXX: workaround for getting a word from compilation
    # stream
    def word(self):
        return self.expect(Word)

    def insert(self, w):
        return self.words.insert(w)

    def switch(self, s):
        if self.state == s:
            # raise Forth_EvaluationError("Unexpected state switch (double :/;)")
            return

        self.state = s

        return s

    def exit(self):
        return ForthSignal.EXIT

    def immediate(self):
        # XXX? Hacky
        # inserting a Non-compile word makes every new word non-compilable
        return self.words.insert(Instruction(name="+immediate", compiled=False))

    def new_word(self, w):
        return self.words.new_word(w)

    # IO

    def run_shell(self, command):
        # TODO @IMPROVEMENT: Generalize the function
        # TODO @WIP:
        #   Implement PIPE/FILE OUTPUT Logic
        c = Command(command)
        return c.execute()

    # evaluation

    def simple_eval(self, instruction):
        return instruction.run(self)

    def eval(self, instruction):
        # I'm cooked
        # FIXME @OVERSIGHT: How does this behave with EXIT?
        if isinstance(instruction, Word):
            return self.eval(self.find(instruction.token))

        if isinstance(instruction, Instruction):
            return instruction.run(self)

        raise Forth_Runtime_EvaluationError(f"Undefined type: {type(instruction)}")

    def exec(self, instructions):
        self.instructions = iter(instructions)

        evaluated = (self.eval(i) for i in instructions)

        results = [
            (report.name, get_instruction_status(report.status)) for report in evaluated
        ]

        return (self.stack, results, self.words.list())

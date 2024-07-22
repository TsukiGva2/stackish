from collections import namedtuple

from .configuration import COMPILE
from .log import Forth_LogInstruction
from .runtime_error import Forth_Runtime_EvaluationError
from .signal import ForthSignal

InstructionStatus = namedtuple("InstructionStatus", ["INTERPRETED", "COMPILED"])


def get_instruction_status(status):
    match status:
        case InstructionStatus.INTERPRETED:
            return "INTERPRETED"
        case InstructionStatus.COMPILED:
            return "COMPILED"
        case _:
            raise KeyError("No such status!")


class InstructionReport:
    def __init__(self, name, status, data):
        self.name = name
        self.data = data
        self.status = status


# This code is really messy and not really well organized
# speed right now is the biggest problem, since the "algorithm"
# is simply a (RUN ALL IN LIST OF LAMBDAS) thing

# instructions are just glorified lambda tuples


class Instruction:
    def __init__(self, *operations, name="_", **flags):
        self.operations = operations

        self.name = name.upper()

        try:
            self.compilable = flags["compiled"]
        except KeyError:
            self.compilable = True

    def __add__(self, other):
        if not isinstance(other, Instruction):
            raise Forth_Runtime_EvaluationError(
                f"Can't add Instruction with type '{type(other)}'"
            )

        return Instruction(
            *(self.operations + other.operations),
            name=f"{self.name} + {other.name}",
            compiled=self.compilable and other.compilable,
        )

    def execute(self, state):
        for op in self.operations:
            if op(state) == ForthSignal.EXIT:
                return ForthSignal.EXIT

        return ForthSignal.OK
        # return ForthSignal.OK if self.repeatable else ForthSignal.EXIT

    def interpret(self, state):
        #       while self.execute(state) == ForthSignal.OK:
        #           ...

        self.execute(state)

        return InstructionReport(
            self.name,
            InstructionStatus.INTERPRETED,
            [],
        )

    def compile(self, state):
        return InstructionReport(
            self.name, InstructionStatus.COMPILED, state.insert(self)
        )

        # print(f"generated: {name}")

    # TODO @OPTIMIZE:
    #   redefine run if compilable so it skips the check
    def run(self, state):
        # neat statement for debug -- TODO @IMPROVEMENT: Improve debugging (logging etc)
        Forth_LogInstruction(self)

        # FIXME @OVERSIGHT:
        # STATE CANT BE BOTH SKIP AND INTERPRET/COMPILE
        # this has no problem right now, however, since
        # the functions IMPLIES(=>) and END(end) which
        # set state to SKIP are both COMPILABLE
        # therefore will not be evaluated when state
        # is not INTERPRET

        # UPDATE: This oversight ended up being significant,
        # because if state is set to SKIP, the operation
        # ends up getting INSERTED as the following
        # condition yields False:

        # not self.compilable (for most this is False) or
        # state.state == -> INTERPRET <- The problem

        # "non-compile" states such as SKIP and INTERPRET
        # have special cases that must be ran (e.g. END, OR)
        # so restricting to only INTERPRET was a bad idea, this
        # code is still XXX though

        # 18/07/24 - Deleted SKIP

        if not self.compilable or state.state != COMPILE:
            return self.interpret(state)

        return self.compile(state)


# alternate dummy instruction type
class Word(Instruction):
    def __init__(self, word):
        self.token = word.upper()

    def run(self, state):
        raise Forth_Runtime_EvaluationError("Trying to run Word type! (use FIND)")

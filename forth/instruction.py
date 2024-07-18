from collections import namedtuple

from .configuration import COMPILE, SKIP

InstructionStatus = namedtuple(
    "InstructionStatus", ["SKIPPED", "INTERPRETED", "COMPILED"]
)


def get_instruction_status(status):
    match status:
        case InstructionStatus.SKIPPED:
            return "SKIPPED"
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

        self.name = name

        try:
            self.compilable = flags["compiled"]
        except KeyError:
            self.compilable = True

        try:
            self.skippable = flags["skippable"]
        except KeyError:
            self.skippable = True

    def skip(self):
        return InstructionReport(self.name, InstructionStatus.SKIPPED, [])

    def interpret(self, state):
        return InstructionReport(
            self.name,
            InstructionStatus.INTERPRETED,
            [op(state) for op in self.operations],
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
        # print(f"{self.name:>10} : {self.skippable} \t| {state.state}\t|N:SKIP:STATE")

        if self.skippable and state.state == SKIP:
            return self.skip()

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

        if not self.compilable or state.state != COMPILE:
            return self.interpret(state)

        return self.compile(state)

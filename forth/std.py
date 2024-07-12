# from .compiler import Compiler
from .configuration import INTERPRET, SKIP
from .instruction import Instruction


class StdFunctions:
    # IO -- FIXME @DESIGN: Implement both at state.io

    # both are XXX
    # TODO @DESIGN @WIP: to Print or to Echo? that is the question
    @staticmethod
    def put():
        return Instruction(lambda state: print(state.drop()))

    # TODO @DESIGN @WIP @OVERSIGHT: handle input elsewhere (state.input?)
    @staticmethod
    def ask():
        return Instruction(lambda state: state.push(input(state.drop())))

    # operators
    @staticmethod
    def add():
        return Instruction(lambda state: state.push(state.drop() + state.drop()))

    @staticmethod
    def sub():
        return Instruction(lambda state: state.push(state.drop() - state.drop()))

    @staticmethod
    def mul():
        return Instruction(lambda state: state.push(state.drop() * state.drop()))

    @staticmethod
    def div():
        return Instruction(lambda state: state.push(state.drop() / state.drop()))

    @staticmethod
    def pow():
        return Instruction(lambda state: state.push(state.drop() ** state.drop()))

    @staticmethod
    def non():
        return Instruction(lambda state: state.push(not state.drop()))

    # logic
    @staticmethod
    def equals():
        return Instruction(lambda state: state.push(state.drop() == state.drop()))

    @staticmethod
    def nequals():
        return Instruction(lambda state: state.push(state.drop() != state.drop()))

    @staticmethod
    def greater():
        return Instruction(lambda state: state.push(state.drop() > state.drop()))

    @staticmethod
    def lesser():
        return Instruction(lambda state: state.push(state.drop() < state.drop()))

    @staticmethod
    def greater_or_equals():
        return Instruction(lambda state: state.push(state.drop() >= state.drop()))

    @staticmethod
    def lesser_or_equals():
        return Instruction(lambda state: state.push(state.drop() <= state.drop()))

    # logic_special
    @staticmethod
    def implies():
        return Instruction(
            lambda state: (state.switch(INTERPRET if state.drop() else SKIP))
        )

    @staticmethod
    def or_word():
        """
        : OR
            _state? 'SKIP = =>
        ;
        """
        return Instruction(
            # _state? =
            lambda state: state.push(state.state == SKIP),
            # =>
            *StdFunctions.implies().operations,
            skippable=False  # cant skip an or
            # otherwise it could
            # not reset the skipping
            # it kinda serves as
            # an alternate end
            # which doubles down
            # as a surprise IMPLIES(=>)
        )

    @staticmethod
    def end():
        return Instruction(
            # NOTE:
            # This doesnt interfere with the COMPILE
            # state at all because of the magic of
            # Instruction flags, the COMPILED flag
            # is set on all instructions by default
            # and an Instruction with the COMPILED
            # flag will not evaluate if the state is
            # set to COMPILED.
            lambda state: state.switch(INTERPRET),
            skippable=False,  # Can't skip an end
            # otherwise the skipping
            # would never... end
        )

    # environment
    # TODO @WIP: Use shell system to get and set env

    # FIXME @WIP -- useless without "state.getenv"
    def env():
        return Instruction(lambda state: state.push(state.getenv(state.drop())))

    # FIXME @WIP -- useless without "state.setenv"
    def setenv():
        return Instruction(
            lambda state: state.setenv(name=state.drop(), value=state.drop())
        )

    # Shell Interaction
    def run_command():
        return Instruction(lambda state: state.push(state.run_shell(state.drop())))

    # useless/misc

    def pop():
        return Instruction(lambda state: state.drop())

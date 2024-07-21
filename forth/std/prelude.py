# from .compiler import Compiler
from forth.configuration import COMPILE, INTERPRET
from forth.instruction import Instruction


class PreludeFunctions:
    # IO -- FIXME @DESIGN: Implement both at state.io

    # both PUT/READ are XXX
    @staticmethod
    def put():
        return Instruction(lambda state: print(state.drop()), name="put")

    # TODO @DESIGN @WIP @OVERSIGHT: handle input elsewhere (state.input?)
    @staticmethod
    def ask():
        return Instruction(lambda state: state.push(input(state.drop())), name="ask")

    # debug word
    @staticmethod
    def peek():
        return Instruction(lambda state: print(state.peek()), name="peek")

    # operators
    @staticmethod
    def add():
        return Instruction(
            lambda state: state.push(state.drop() + state.drop()), name="add"
        )

    @staticmethod
    def sub():
        return Instruction(
            lambda state: state.push(state.drop() - state.drop()), name="sub"
        )

    @staticmethod
    def mul():
        return Instruction(
            lambda state: state.push(state.drop() * state.drop()), name="mul"
        )

    @staticmethod
    def div():
        return Instruction(
            lambda state: state.push(state.drop() / state.drop()), name="div"
        )

    @staticmethod
    def pow():
        return Instruction(
            lambda state: state.push(state.drop() ** state.drop()), name="pow"
        )

    @staticmethod
    def non():
        return Instruction(lambda state: state.push(not state.drop()), name="non")

    @staticmethod
    def swap():
        return Instruction(lambda state: state.swap(), name="swap")

    @staticmethod
    def dup():
        return Instruction(lambda state: state.dup(), name="dup")

    # logic
    @staticmethod
    def equals():
        return Instruction(
            lambda state: state.push(state.drop() == state.drop()), name="equals"
        )

    @staticmethod
    def nequals():
        return Instruction(
            lambda state: state.push(state.drop() != state.drop()), name="nequals"
        )

    @staticmethod
    def greater():
        return Instruction(
            lambda state: state.push(state.drop() > state.drop()), name="greater"
        )

    @staticmethod
    def lesser():
        return Instruction(
            lambda state: state.push(state.drop() < state.drop()), name="lesser"
        )

    @staticmethod
    def greater_or_equals():
        return Instruction(
            lambda state: state.push(state.drop() >= state.drop()),
            name="greater_or_equals",
        )

    @staticmethod
    def lesser_or_equals():
        return Instruction(
            lambda state: state.push(state.drop() <= state.drop()),
            name="lesser_or_equals",
        )

    # FIXME @WIP:
    #    # logic_special
    #    @staticmethod
    #    def implies():
    #        return Instruction(
    #            lambda state: (state.switch(INTERPRET if state.drop() else SKIP)),
    #            name="implies",
    #        )

    #    @staticmethod
    #    def or_word():
    #        """
    #        : OR
    #            _state? 'SKIP = =>
    #        ;
    #        """
    #        return Instruction(
    #            # _state? =
    #            lambda state: state.push(state.state == SKIP),
    #            # =>
    #            *PreludeFunctions.implies().operations,
    #            skippable=False,  # cant skip an or
    #            # otherwise it could
    #            # not reset the skipping
    #            # it kinda serves as
    #            # an alternate end
    #            # which doubles down
    #            # as a surprise IMPLIES(=>)
    #            name="or"
    #        )

    #    @staticmethod
    #    def end():
    #        return Instruction(
    #            # NOTE:
    #            # This doesnt interfere with the COMPILE
    #            # state at all because of the magic of
    #            # Instruction flags, the COMPILED flag
    #            # is set on all instructions by default
    #            # and an Instruction with the COMPILED
    #            # flag will not evaluate if the state is
    #            # set to COMPILED.
    #            lambda state: state.switch(INTERPRET),
    #            skippable=False,  # Can't skip an end
    #            # otherwise the skipping
    #            # would never... end
    #            name="end",
    #        )

    # TODO @WIP:
    """
    CREATE :
    DOES>
        WORD

    @staticmethod
    def colon():
        return Instruction(
            lambda state: state.switch(COMPILE),
            lambda state: state.open_header(),
            compiled=False,
            name="colon",
        )

    @staticmethod
    def endcolon():
        return Instruction(
            lambda state: state.switch(INTERPRET),
            lambda state: state.close_header(),
            compiled=False,
            name="end_word_def",
        )
    """

    @staticmethod
    def compile():
        return Instruction(lambda state: state.switch(COMPILE), name="compile")

    @staticmethod
    def interpret():
        return Instruction(
            lambda state: state.switch(INTERPRET), name="interpret", compiled=False
        )

    @staticmethod
    def words():
        return Instruction(lambda state: print(state.word_table()), name="words")

    # Get a word from input
    @staticmethod
    def word():
        return Instruction(lambda state: state.word(), name="word")

    # EXIT an instruction
    @staticmethod
    def exit():
        return Instruction(lambda state: state.exit(), name="exit")

    @staticmethod
    def create():
        """
        Non standard compliant, functionality REALLY simplified

        : CREATE ( -- )
            WORD
            state.new_word(): pop()
        ;
        """
        return PreludeFunctions.word() + Instruction(
            lambda state: state.new_word(state.drop()), name="create"
        )

    @staticmethod
    def immediate():
        return Instruction(
            lambda state: state.immediate(), name="immediate", compiled=False
        )

    @staticmethod
    def colon():
        """
        DEFINE :
            CREATE
            COMPILE
        END
        """
        return PreludeFunctions.create() + PreludeFunctions.compile()

    @staticmethod
    def semicolon():
        """
        DEFINE ;
            INTERPRET
        END
        """
        return PreludeFunctions.interpret()

    @staticmethod
    def branch():
        """
        : IF
            WORD
        ;
        """
        return Instruction()

    # environment
    # TODO @WIP: Use shell system to get and set env

    # FIXME @WIP -- useless without "state.getenv"
    @staticmethod
    def env():
        return Instruction(
            lambda state: state.push(state.getenv(state.drop())), name="env"
        )

    # FIXME @WIP -- useless without "state.setenv"
    @staticmethod
    def setenv():
        return Instruction(
            lambda state: state.setenv(name=state.drop(), value=state.drop()),
            name="setenv",
        )

    # Shell Interaction
    @staticmethod
    def run_command():
        return Instruction(
            lambda state: state.push(state.run_shell(state.drop())), name="run_command"
        )

    # useless/misc

    @staticmethod
    def pop():
        return Instruction(lambda state: state.drop(), name="pop")

    @staticmethod
    def nop():
        return Instruction(name="NO-OP")

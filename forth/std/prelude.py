# from .compiler import Compiler
from collections import OrderedDict

from forth.configuration import COMPILE, INTERPRET
from forth.instruction import Instruction
from forth.types import forth_type_to_string


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
        return Instruction(lambda state: state.display_words(), name="words")

    @staticmethod
    def reset():
        return Instruction(lambda state: state.reset_words(), name="reset")

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

    # NOTE:
    # The following are replacements to the forth words BRANCH
    # and BRANCH0
    @staticmethod
    def until():
        """
        single-word conditional looping

        UNTIL <COND>

        example:

        : CHECK WORD DUP 'then = ;
        UNTIL CHECK
        """
        return PreludeFunctions.word() + Instruction(
            lambda state: state.until(forth_type_to_string(state.drop()))
        )

    @staticmethod
    def until0():
        """
        Conditional UNTIL, runs the until word if stack value is not truthful
        UNTIL0 <type>
        """
        return PreludeFunctions.word() + PreludeFunctions.swap() + Instruction()

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


Prelude = OrderedDict(
    {
        # IO
        ".": PreludeFunctions.put(),
        "READ": PreludeFunctions.ask(),
        "PEEK": PreludeFunctions.peek(),
        # operators
        "+": PreludeFunctions.add(),
        "-": PreludeFunctions.sub(),
        "/": PreludeFunctions.div(),
        "*": PreludeFunctions.mul(),
        "^": PreludeFunctions.pow(),
        "~": PreludeFunctions.non(),
        # logic
        "=": PreludeFunctions.equals(),
        "~=": PreludeFunctions.nequals(),
        ">": PreludeFunctions.greater(),
        "<": PreludeFunctions.lesser(),
        ">=": PreludeFunctions.greater_or_equals(),
        "<=": PreludeFunctions.lesser_or_equals(),
        # IF THEN
        # "IF": PreludeFunctions.implies(),     -- FIXME @WIP
        # "OR": PreludeFunctions.or_word(),     -- FIXME @WIP
        # "ELSE": PreludeFunctions.else_word(), -- FIXME @WIP
        # "THEN": PreludeFunctions.end(),       -- FIXME @WIP
        # FUNCTIONS
        ":": PreludeFunctions.colon(),
        ";": PreludeFunctions.semicolon(),
        "CREATE": PreludeFunctions.create(),  # exposing the POWER
        "WORD": PreludeFunctions.word(),
        "WORDS": PreludeFunctions.words(),
        "RESET": PreludeFunctions.reset(),
        # environment
        "$": PreludeFunctions.env(),
        "EXPORT": PreludeFunctions.setenv(),
        # Shell
        "?": PreludeFunctions.run_command(),
        # "|": PreludeFunctions.pipe(),         -- FIXME @WIP
        # "<-": PreludeFunctions.tofile(),      -- FIXME @WIP
        # State                                 -- TODO @DESIGN @WIP:
        #                                           Not really focused on state atm
        # "@": PreludeFunctions.fetchvar(),
        # "!": PreludeFunctions.definevar(),
        # Misc
        "SWAP": PreludeFunctions.swap(),
        "DUP": PreludeFunctions.dup(),
        "-.": PreludeFunctions.pop(),  #        -- FIXME: Lmao this string is literally invalid
    }
)

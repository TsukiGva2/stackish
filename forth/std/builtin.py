from forth.instruction import Instruction, Word


class BuiltinFunctions:
    """
    Functions defined at the outer compiler level
    """

    # Create/Immediate are defined using WORD (next)
    @staticmethod
    def create(compiler_state):
        """
        CREATE :
        DOES>
            CREATE
            HERE
        """
        w = compiler_state.next()
        return Instruction(lambda state: state.create_header_word(w), name="create")

    @staticmethod
    def immediate(compiler_state):
        w = compiler_state.next()
        return Instruction(
            lambda state: state.immediate_find(w), compiled=False, name="immediate"
        )

    @staticmethod
    def word(w):
        return Word(w)

    @staticmethod
    def literal(n):
        return Instruction(lambda state: state.push(n), name="literal")

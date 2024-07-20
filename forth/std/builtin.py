from forth.instruction import Instruction, Word


class BuiltinFunctions:
    """
    Functions defined at the outer compiler level
    """

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

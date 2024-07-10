from .configuration import INTERPRET


class Instruction:
    def __init__(self, *operations, name="_", compiled=True):
        self.operations = operations

        self.name = name
        self.compiled = compiled

        # print(f"generated: {name}")

    def run(self, state):
        if not self.compiled or state.state == INTERPRET:
            return [op(state) for op in self.operations]

        return state.insert(self)

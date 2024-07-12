from .configuration import INTERPRET, SKIP

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

        # print(f"generated: {name}")

    # TODO @OPTIMIZE:
    #   redefine run if compilable so it skips the check
    def run(self, state):
        #print(f"{self.name} : {self.skippable}")
        if self.skippable and state.state == SKIP:
            return []

        # FIXME @OVERSIGHT:
        # STATE CANT BE BOTH SKIP AND INTERPRET/COMPILE
        # this has no problem right now, however, since
        # the functions IMPLIES(=>) and END(end) which
        # set state to SKIP are both COMPILABLE
        # therefore will not be evaluated when state
        # is not INTERPRET

        if not self.compilable or state.state == INTERPRET:
            return [op(state) for op in self.operations]

        return state.insert(self)

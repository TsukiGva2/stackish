from .configuration import COMPILE, SKIP

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
        # neat statement for debug -- TODO @IMPROVEMENT: Improve debugging (logging etc)
        # print(f"{self.name:>10} : {self.skippable} \t| {state.state}")

        if self.skippable and state.state == SKIP:
            return []

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
            return [op(state) for op in self.operations]

        return state.insert(self)

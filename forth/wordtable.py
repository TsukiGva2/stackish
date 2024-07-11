from .configuration import HEADER_EMPTY
from .std import StdFunctions


class WordHeader:
    def __init__(self, header=HEADER_EMPTY):
        self.header = header
        self.instructions = []

    def pack(self):
        return {self.header: self.instructions}

    def clear(self):
        self.header = HEADER_EMPTY
        self.instructions = []

    def insert(self, instruction):
        self.instructions.append(instruction)


# FMT
# '(file name \.) fmt

"""
    # (filename -- msg)     # specifying arguments (optional but recommended)
    : exists?               # defining a function

        # setting a return message

        '(file exists)      # push return message to the stack
        swap                # swap return message and file name

        dup                 # duplicating file name so we can still use it later

        '(no such file \.)  # push error message to the stack
        fmt                 # formatting (substitutes any \. in the string with a value from the stack)

        swap                # swap return message and file name


        # building a command

        '(stat \.)          # adding '(stat) to the stack
        fmt


        # running the command

        ?                   # run 'stat' command and get return value


        # conditional execution

        =>                  # if return value is a success status then

            swap            # swap return message ('no such file' was pushed last so we gotta switch)

        end                 # end if statement

        dup                 # duplicating the return value (so we can print it and still return)
        .                   # print return message (top element on the stack)

    ;                       # ending function definition

    # dummy example
    : writesafe ( file str -- )
        swap
        exists? '(file exists) =
        =>
            '()
        end
    ;
"""

# - ls
# .git/ main.py
# - 'main.py exists?
# [main.py, file exists]
# [file exists, main.py]
# [file exists, main.py, main.py, no such file]
# [file exists, main.py, no such file main.py]
# [file exists, no such file main.py, main.py]
# [file exists, no such file main.py, main.py, stat \.]
# [file exists, no such file main.py, stat main.py]
# [file exists, no such file main.py, 0 (SUCCESS)]
# [no such file main.py, file exists]
# [no such file main.py, file exists, file exists]
# [no such file main.py, file exists]
# OK. FILE EXISTS.


# read -> input()

# + -> push(): pop() + pop()
# - -> push(): pop() - pop()
# / -> push(): pop() / pop()
# * -> push(): pop() * pop()
# ^ -> push(): pop() ^ pop()
# ~ -> push(): ~ pop()

# = -> push(): pop() == pop()
# ~= -> push(): pop() != pop()
# > -> push(): pop() > pop()
# < -> push(): pop() < pop()
# >= -> push(): pop() >= pop()
# <= -> push(): pop() <= pop()

# => -> if not pop() then state = SKIP
# +noskip end -> state = INTERPRET

"""
+noskip
: or
    state?
;
"""

# $ -> push(): ( getenv(): ENV=pop() )
# export -> push(): ( setenv(): ENV=pop() VAL=pop() )

# TODO: these commands need a PIPE

"""
PROTO SHELL -> [TODO:shell.run()] as Run()

: SHELL ( PIPE cmd -- )
    swap
    dup

    pipe? => swap Run(): pop() pop()
    or Run(): pop()
;
"""

# ? -> SHELL():

"""
2 2 =
=> INTERPRET

    1 2 => SKIP
    end INTERPRET

    3 3 => INTERPRET

        2 4 => SKIP

        end INTERPRET

        4 4 => INTERPRET

        end INTERPRET

    end INTERPRET

end INTERPRET
"""


class WordTable:
    def __init__(self):
        self.words = {
            # IO
            # ".": StdFunctions.put(), # : . '(echo) ? ;
            "read": StdFunctions.ask(),
            # operators
            "+": StdFunctions.add(),
            "-": StdFunctions.sub(),
            "/": StdFunctions.div(),
            "*": StdFunctions.mul(),
            "^": StdFunctions.pow(),
            "~": StdFunctions.non(),
            # logic
            "=": StdFunctions.equals(),
            "~=": StdFunctions.nequal(),
            ">": StdFunctions.greater(),
            "<": StdFunctions.lesser(),
            ">=": StdFunctions.geq(),
            "<=": StdFunctions.leq(),
            "=>": StdFunctions.implies(),
            "end": StdFunctions.end(),
            # environment
            "$": StdFunctions.env(),
            "export": StdFunctions.setenv(),
            # Shell
            "?": StdFunctions.shell(),
            "|": StdFunctions.pipe(),
            "<-": StdFunctions.tofile(),
            # State
            "@": StdFunctions.fetchvar(),
            "!": StdFunctions.definevar(),
            # Misc
            "-.": StdFunctions.pop(),
        }

        self.header = WordHeader()

    def new(self, w):
        self.header = WordHeader(w)
        return w

    def end(self):
        name = self.header.header

        self.words.update(self.header.pack())
        self.header.clear()

        return name

    def insert(self, instruction):
        self.header.insert(instruction)

        return instruction.name

    def find(self, w):
        return self.words[w]

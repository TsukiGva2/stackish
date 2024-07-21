# TODO @IMPROVEMENT:
# use a logging library
import inspect

# me when the whole program doesnt use regexes but
# the LOGGING module does
import re


# XXX: better logging
def Forth_Log(s):
    print(s)


# XXX: all of this is temporary
def pretty_operation(operation):
    o = inspect.getsource(operation)
    return " ".join(  # replace all whitespace with a single space
        re.sub(
            r'Instruction\(|return|lambda:|lambda state:|state\.|name=".+"|,|\)$', "", o
        ).split()
    )


# XXX @WIP: what
def Forth_LogInstruction(instruction):
    sources = " + ".join([f"{pretty_operation(op)}" for op in instruction.operations])
    Forth_Log(f"\tNAME: {instruction.name}\n\tCODE: {sources}\n")

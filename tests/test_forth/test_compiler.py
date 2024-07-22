from forth.compiler import Compiler
from forth.instruction import Word


def test_compiler_literals():
    compiler = Compiler()

    compileTest = "'quote '(multiple quote) 1"

    instructions = compiler.compile(compileTest)

    for i in instructions:
        assert i.name == "LITERAL"


def test_compiler_words():
    compiler = Compiler()

    compileTest = "foo"

    instructions = compiler.compile(compileTest)

    assert isinstance(instructions[-1], Word)

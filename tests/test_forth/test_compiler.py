from forth.compiler import Compiler


def test_compiler_literals():
    compiler = Compiler()

    compileTest = "'quote '(multiple quote) 1 1.0 1e6 -1 -1e6"

    instructions = compiler.compile(compileTest)

    for i in instructions:
        assert i.name == "literal"


def test_compiler_find():
    compiler = Compiler()

    compileTest = "foo 'literal"

    expected_instructions = ["find", "literal"]

    instructions = compiler.compile(compileTest)

    for instruction, expected in zip(instructions, expected_instructions):
        assert instruction.name == expected

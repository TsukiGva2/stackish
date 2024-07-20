from forth.system import System


def test_runtime_literals():
    system = System()

    stack, reports, words = system.do_string("'foo '(bar) 1 1e6")

    assert all(("foo" in stack, "bar" in stack, 1 in stack, 1e6 in stack))


def test_function_definition():
    system = System()

    stack, reports, words = system.do_string(": foo 'testing! ; foo")

    assert "foo" in words
    assert "testing!" in stack

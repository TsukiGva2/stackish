# v0.2.1 - WIP

## General

### Minor changes

- Fixed typo in the `expect` function, which was defined as `expecting`
- Improved COMMENTS.md to clarify other types of comments
- Marked DOCUMENTATION.md as a TODO, it's currently a mess. Please don't consult it

### Mid changes

- Changed definition of the Word class, now extending Instruction **__(1)__**
- All errors now extend Exception instead of the mess it was **__(2)__**

- Changed test cases to improve readability, the tests are still not fine tuned and kinda useless

**1.**

    Also had to invert the order at runtime so it checks whether
    `instruction' argument is of type Word, then of type Instruction

    Relevant code (comments are just for extra description, not included in the code):

__@ forth/instruction.py__

```py
...
class Word(Instruction):
#          ^^^^^^^^^^^ <- now extending instruction

+    def __init__(self, word):
+        self.token = word

+    def run(self, state):
+        raise Forth_EvaluationError("Trying to run Word type! (use FIND)")

$
```

__@ forth/runtime.py__

```diff
    ...

    def eval(self, instruction):
        if self.expecting is not None:
            return self.expect(instruction)

+       if isinstance(instruction, Word):
+           return self.eval(self.find(instruction.token))
-       if isinstance(instruction, Instruction):
-           return instruction.run(self)

+       if isinstance(instruction, Instruction):
+           return instruction.run(self)
-       if isinstance(instruction, Word):
-           return self.eval(self.find(instruction.token))
        ...

    ...
```

**2.**

    Proper (custom) exception handling is still a topic i lack understanding,
    so i'll leave it on hold until it's a better time in development
    for implementing them.

---

# v0.2.0 - WIP

## General

- Started keeping track of relatively big changes thru CHANGELOG.md

## Significant runtime changes

- Moved FIND logic out of the compiler to Runtime **__(1)__**
- Removed WordHeader related functions, now they are WIP again **__(2)__**

- Added 'WORD' for fetching the next word from 'input' **__(3)__**

### 'WordTable' related

### Significant changes

- Moved if/else logic to WIP, rethinking the skipping logic
- Moved function definition logic to WIP, looking for a full rework **__(4)__**
- Removed WordHeader logic, expect all of it gone in the next update **__(5)__**

### Mid changes
- (renamed) wordtable.py -> words.py **__(6)__**

**1.**

    This has to do with me willing to get closer to the forth
    standard, the objective is getting a better general understanding
    and also optimizing the compiler, which is meant to be simple.

**2.**

    All WIP, hated that piece of code, hoping it will be all gone soon,
    the inner workings were confusing and just a wrapping mess. Looking
    for a more functional approach, also closer to the forth standard.

**3.**

    This addition involved the inclusion of several other
    methods, here is the relevant code/commentary

__@ forth/runtime.py__

```py

    ...

+    def expecting(self, instruction):
+        assert isinstance(instruction, self.expecting)
+
+        if self.expecting == Word:
+            self.expecting = None
+
+            return self.simple_eval(BuiltinFunctions.literal(instruction.token))
+
+        raise Forth_NotImplemented("Can't expect a non-word value")

    ...

    ...

+    # TODO @WIP XXX: this 'expected_type' logic reveals a
+    # larger issue with this implementation, hinting that
+    # possibly the compiler and runtime are not well integrated,
+    # forcing it to emulate getting a WORD from 'input', for example
+
     def eval(self, instruction):
+        if self.expecting is not None:
+            return self.expect(instruction)

        ...

    ...
```

__@ forth/std/prelude.py__

```py
    ...

+    @staticmethod
+    def word():
+        return Instruction(lambda state: state.word(), name="word")

    ...
```

**4.**

    The rework is related to the creation of the CREATE word, which i
    think it's an amazing idea, being a big fan of metaprogramming myself.

**5.**

    Repeating myself here, but, it's a mess

**6.**

    Renaming for clarity, makes a little more sense now


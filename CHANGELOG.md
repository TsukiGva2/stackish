# v0.2.0 - WIP

## General

- Started keeping track of relatively big changes thru CHANGELOG.md

## Significant runtime changes

- Moved FIND logic out of the compiler to Runtime (1)
- Removed WordHeader related functions, now they are WIP again (2)

- Added 'WORD' for fetching the next word from 'input' (3)

### 'WordTable' related

### Significant changes

- Moved if/else logic to WIP, rethinking the skipping logic
- Moved function definition logic to WIP, looking for a full rework (4)
- Removed WordHeader logic, expect all of it gone in the next update (*5)

### Mid changes
- (renamed) wordtable.py -> words.py (6)

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


# Usable example

```
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
```

### Output:

```
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
```

# NOTE: String Formatting
*NOT IMPLEMENTED @WIP*

### Dot syntax: any '\\.'s are substituted by {pop()}

```
'(file name \.) fmt
```

# Basic word Implementations

## . -> print(): pop()
## read -> push(): input()

## + -> push(): pop() + pop()
## - -> push(): pop() - pop()
## / -> push(): pop() / pop()
## * -> push(): pop() * pop()
## ^ -> push(): pop() ^ pop()
## ~ -> push(): ~ pop()

## = -> push(): pop() == pop()
## ~= -> push(): pop() != pop()
## > -> push(): pop() > pop()
## < -> push(): pop() < pop()
## >= -> push(): pop() >= pop()
## <= -> push(): pop() <= pop()

## ... -> no-op
---

# Conditional execution

## => -> if not pop() then state = SKIP
## +noskip end -> state = INTERPRET

### TABLE: Analysing how SKIP works
```
-------------------------------------------------------
  FUNCTION      |         STATE         |   ATTRIBUTE
-------------------------------------------------------
2 2 =
=>                      INTERPRET
    1 2 = =>            SKIP
        'what .
    end                 INTERPRET           +noskip
    3 3 = =>            INTERPRET
        2 4 = =>        SKIP
            'what .
        end             INTERPRET           +noskip
        4 4 = =>        INTERPRET
            'ok .
        end             INTERPRET           +noskip
    end                 INTERPRET           +noskip
end                     INTERPRET           +noskip
```

### As implemented in forth/instruction.py
```py
    # ... (on Instruction.__init__)
        try:
            self.skippable = flags["skippable"]
        except KeyError:
            self.skippable = True
    # ...

    def run(self, state):
        if self.skippable and state.state == SKIP:
            return []
    
    # ...
```

## OR:

```
+noskip
: or
    state? 'SKIP = =>
;
```

### EXAMPLE:
```
    '/bin/sh exists? '(file exists) =
    =>
        ...
    or
        ...
    end
```
---

# Shell/Environment

## $ -> push(): ( getenv(): ENV=pop() )
## export -> push(): ( setenv(): ENV=pop() VAL=pop() )

- TODO: the following commands need a PIPE implementation

```
: SHELL ( cmd pipe -- _Process )
    dup

    pipe? => swap 
    or Run(1)
    end
;
```

---
### TODO @OVERSIGHT @WIP:
###   Processes are currently waited for in the Command() class.
###   Create a way to run them and not wait() right away, so we can
###   PIPE its output to a file or another Command()
---

## -- NOTE: Wait is done automatically atm (see above)
## ~status -> waitProcess(): process? pop()~

## toFile -> processToFile(): process? pop()

## ? -> SHELL status

## | -> SHELL -- NOTE: do we even need this?

## '<-' -> SHELL toFile

# Misc/Useless

## -. -> pop()


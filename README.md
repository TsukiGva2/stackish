# stackish
A shell using a language inspired in forth (called stackish) as the scripting language


# The Language

The language is designed for use in an interactive environment
(i.e. a shell), it has a LOT of differences from classic Forth
for the following reasons:

- It's not designed to be embeddable (It's also implemented in python, so...)
- It's not designed to micro manage memory
- It's not designed around cells (no size/memory constraints)
- It's not designed to be fast (optimization is not the main focus right now)

Although i intend to keep my implementation closer to standard forth
in the future. But for this i need to get a deeper understanding, which
i'm still developing.

## Objectives/Vision

The language is designed to integrate with the shell environment
and extend it, providing better scripting capabilities, preferably
entirely from the command line, without ever loading code from files.

### How would that be possible?

The answer is modularity, through the definition of a set of
reusable, general functions, solving bigger problems becomes
a matter of finding the right tools.

**Example**

The simplest example is running actual programs from the shell,
this is done by running `'(command) ?`. It may seem inconvenient (it is),
but any command can (and is intended to) be wrapped in a word definition, with a
descriptive name, like the following session example:

```forth
    - ls
      ^^ undefined word

    - '(ls -la) ?
    drwxr--r-- ... .git/
    drwxr--r-- ... stackish
    ...

    - : list-all '(ls -la) ? ;
    OK 'list-all

    - list-all
    drwxr--r-- ... .git/
    drwxr--r-- ... stackish
    ...
    -
```


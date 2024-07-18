# STATES
INTERPRET = 0
COMPILE = 1
SKIP = 2

# DELIMS
DELIM_QUOTE_BEGIN = "'("
DELIM_QUOTE_END = ")"

DELIM_SQUOTE_BEGIN = "'"
DELIM_SQUOTE_END = None  # applies to one word

INDEX_QUOTE_BEGIN = len(DELIM_QUOTE_BEGIN)
INDEX_QUOTE_END = -len(DELIM_QUOTE_END)

INDEX_SQUOTE_BEGIN = len(DELIM_SQUOTE_BEGIN)
# INDEX_SQUOTE_END = -len(DELIM_SQUOTE_END)

HEADER_EMPTY = "_"

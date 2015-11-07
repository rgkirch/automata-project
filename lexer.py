import sys, collections

try:
    input_file = sys.argv[1]
except IndexError:
    print( "Error, no input file.", file=sys.stderr )
    sys.exit(1)

ASSERT = r"assert"
ASSIGN = r"assign"
ELSE = r"else"
EQUALITY = r"=="
GREATER = r">"
ID = r"[a-za-z]([0-9a-zA-Z_])*"
IF = r"if"
LBRACE = r"{"
LPAREN = r"}"
NAT = r"0|[1-9]+"
NOT = r"!"
OR = r"||"
PRINTNAT = r"printNat"
RBRACE = r"}"
READNAT = r"readNat"
RPAREN = r")"
SEMICOLON = r";"
WHILE = r"while"

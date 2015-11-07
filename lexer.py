import sys, collections, re

ASSERT = r"assert"
ASSIGN = r"="
ELSE = r"else"
EQUALITY = r"=="
GREATER = r">"
IF = r"if"
LBRACE = r"{"
LPAREN = r"\("
MAIN = r"main"
NOT = r"!"
OR = r"\|\|"
PRINTNAT = r"printNat"
RBRACE = r"}"
READNAT = r"readNat"
RPAREN = r"\)"
SEMICOLON = r";"
WHILE = r"while"
NAT = r"0|[1-9]+"
ID = r"[a-zA-Z][0-9a-zA-Z_]*"

tokens = [ASSERT, ASSIGN, ELSE, EQUALITY, GREATER, IF, LBRACE, LPAREN, MAIN, NOT, OR, PRINTNAT, RBRACE, READNAT, RPAREN, SEMICOLON, WHILE, NAT, ID]
token_str = ["ASSERT", "ASSIGN", "ELSE", "EQUALITY", "GREATER", "IF", "LBRACE", "LPAREN", "MAIN", "NOT", "OR", "PRINTNAT", "RBRACE", "READNAT", "RPAREN", "SEMICOLON", "WHILE", "NAT", "ID"]

alternate = "(" + ")|(".join(tokens) + ")"
#regex = list( map(re.compile, tokens) )


with open( input_file, "r" ) as f:
    data = f.read()
    finds = re.findall(re.compile(alternate), data)
for group in finds:
    for index,t in enumerate(group):
        if t:
            print( token_str[index], end=" ")

#try:
#    input_file = sys.argv[1]
#except IndexError:
#    print( "Error, no input file.", file=sys.stderr )
#    sys.exit(1)
#def producer(name):
#    whitespace = re.compile(r"\s")
#    comment = re.compile(r"//")
#    with open(name, "r") as f:
#        for line in f:
#            for char in line:
#                if not whitespace.match(char):
#                    yield char

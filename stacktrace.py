# Given a string, and an LL(1) parse table, determine
# if the string is in the given language

# representation of LL(1) parse table, for testing purposes
parseTable = { "E" : {"(" : "TY", "n" : "TY"},
        "Y" : {"+" : "+TY", ")" : "", "$" : ""},
        "T" : {"(" : "FX", "n" : "FX"},
        "X" : {"+" : "", "*" : "*FX", ")" : "", "$" : ""}
        "F" : {"(" : "(E)", "F" : "n"}}

def run_stacktrace(instring):
    # check that terminals in input string are in grammar
    for sym in instring:
        if sym not in nonterminals:
            print("error: '{sym}' not in grammar".format())
    
    # create stack and push startSymbol
    stack = [startSymbol]

    while True:
        # compare input symbol with `

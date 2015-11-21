import grammar

# representation of LL(1) parse table, for testing purposes
exampleParseTable = { "E" : {"(" : "TY", "n" : "TY"},
        "Y" : {"+" : "+TY", ")" : "", "$" : ""},
        "T" : {"(" : "FX", "n" : "FX"},
        "X" : {"+" : "", "*" : "*FX", ")" : "", "$" : ""},
        "F" : {"(" : "(E)", "n" : "n"}}

# Given a string, and an LL(1) parse table, determine
# if the string is in the given language
def run_stacktrace(grammar, inputstring):
    # check that terminals in input string are in grammar
    for sym in inputstring:
        if sym not in grammar.terminals:
            print("error: '{}' not in grammar".format(sym))
            return
    if inputstring[-1] != '$':
        inputstring += '$'
    
    # create stack and push startSymbol
    stack = [grammar.startSymbol]
    
    currentsym = inputstring[0] # current symbol at front of input string
    symindex = 1
    steps = [] # track of the state of the stack and input string at each step
    while True: 
        if not stack and currentsym == '$':
            steps.append((inputstring, "empty"))
            printtrace(steps)
            break
        # if currentsym == ToS pop sym of stack and advance one sym
        if currentsym == stack[-1]:
            print([i for i in stack])
            stack.pop()
            currentsym = inputstring[symindex]
            symindex += 1
        else:
            # print(currentsym, stack[-1])
            print([i for i in stack])
            top = stack.pop()
            try:
                stack.extend(list(grammar.parseTable[top][currentsym])[::-1])
                steps.append((inputstring[symindex:], stack))
            except IndexError:
                steps.append((inputstring, "error"))
                printtrace(steps)
                print("No action defined for input symbol {}, when {} is at top of stack".format(
                    currentsym, top))
                
# prints the stacktrace in a pretty readable way, data is a list of 2-tuples
# corresponding (1) input, and (2) current stack, the default parameter delay
# will cause a sleep for n seconds between printing steps
def printtrace(steps, delay=0):
    # print column headers
    colhdrs = "{0:<{1}} | step # | stack".format("input", len(inputstring)-len("input"))
    print(colhdrs)
    print("-" * len(colhdrs))
    # print the rest of the data
    count = 1
    for i in steps[:-1]:
        print("{0:<{1}} | {2:^8} | {3}".format(i[0], ''.join(i[1])))

def prompt():
    print("Determine if a string is in a given LL(1) grammar")

if __name__ == "__main__":
    prompt()
    g = grammar.Grammar()
    g.parseTable = exampleParseTable
    g.startSymbol = 'E'
    g.terminals = ['+', '*', '(', ')', 'n', '$']
    inputstring = input("Enter a string to check (empty string to quit): ")
    while inputstring:
       run_stacktrace(g, inputstring)
       inputstring = input("Enter a string to check (empty string to quit): ")

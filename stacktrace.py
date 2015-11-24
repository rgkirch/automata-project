import sys, time
import grammar

# representation of LL(1) parse table, for testing purposes
exampleParseTable1 = { 
        "E" : {"(" : "TY", "n" : "TY"},
        "Y" : {"+" : "+TY", ")" : "", "$" : ""},
        "T" : {"(" : "FX", "n" : "FX"},
        "X" : {"+" : "", "*" : "*FX", ")" : "", "$" : ""},
        "F" : {"(" : "(E)", "n" : "n"}
        }
startSymbol1 = 'E'
terminals1 = ['+', '*', '(', ')', 'n', '$']
exampleParseTable2 = { 
        "S" : {"0" : "E"},
        "E" : {"0" : "TA"},
        "A" : {"+" : "+TA", "$" : ""},
        "T" : {"0" : "0"}
        }
startSymbol2 = 'S'
terminals2 = ['+', '0', '$']
# Given a string, and an LL(1) parse table, determine if the string is in the
# given language, returns a list of of tuples, where each tuple contains
# (1) the remaining input string (2) current state the stack or an accept, or
# error message
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
    # track of the state of the stack and input string at each step
    steps = [(inputstring, ''.join(stack[::-1]))] 
    while True: 
        if not stack and inputstring[0] == '$':
            steps.pop()
            steps.append((inputstring, 'accept'))
            break
        # if currentsym == ToS pop sym of stack and advance one sym
        if inputstring[0] == stack[-1]:
            stack.pop()
            inputstring = inputstring[1:]
            steps.append((inputstring, ''.join(stack[::-1])))
        else:
            top = stack.pop()
            try:
                stack.extend(list(grammar.parseTable[top][inputstring[0]])[::-1])
                steps.append((inputstring, ''.join(stack[::-1])))
            except IndexError:
                steps.append((inputstring, "error"))
                break
            except KeyError:
                steps.append((inputstring, "error"))
                break
            try:
                grammar.parseTable[top]
            except KeyError:
                print("keyerror on", top)

    return steps 
# prints the stacktrace in a pretty readable way, data is a list of 2-tuples
# corresponding (1) input, and (2) current stack, the default parameter delay
# will cause a sleep for n seconds between printing steps
def printtrace(steps, delay=0):
    # print column headers
    input_colwidth= len(steps[0][0]) if len(steps[0][0]) else len("input")
    colhdrs = "{0:<{1}} | step | stack".format("input", input_colwidth)
    print(colhdrs)
    print("-" * len(colhdrs))
    # print the rest of the data
    count = 1
    for i in steps[:-1]:
        print("{0:<{1}} | {2:^4} | {3}".format(i[0], input_colwidth, count, i[1]))
        count += 1
        time.sleep(delay)
    
    print("{0:<{1}} | {2:^4} | {3}".format(steps[-1][0], input_colwidth, count, steps[-1][1]))

def prompt():
    print("Determine if a string is in a given LL(1) grammar")

if __name__ == "__main__":
    prompt()
    g = grammar.Grammar()
    if len(sys.argv[1:]):
        with open(sys.argv[1], 'r') as f:
            g.buildGrammar(f)
            g.buildParseTable()
            inputstring = input("Enter a string to check (empty string to quit): ")
            while inputstring:
                trace = run_stacktrace(g, inputstring)
                printtrace(trace, 0)
                inputstring = input("Enter a string to check (empty string to quit): ")
    else:
        g.buildGrammar()
        g.buildParseTable()
        #g.parseTable = exampleParseTable2
        #g.startSymbol = startSymbol2
        #g.terminals = terminals2
        inputstring = input("Enter a string to check (empty string to quit): ")
        while inputstring:
            trace = run_stacktrace(g, inputstring)
            printtrace(trace, 0)
            inputstring = input("Enter a string to check (empty string to quit): ")

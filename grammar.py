from collections import OrderedDict
from functools import reduce
import sys

class Grammar:
#terminals = ["+*$"]
#rules = \
#{
#    "S":["E$"],
#    "A":["+TA"],
#    "E":["TA"],
#    "B":["*FB"],
#    "T":["FB"],
#    "F":["(E)", "x"]
#}
    def __init__(self):
        self.grammar = OrderedDict()
        self.terminals = []
        self.parseTable = {}
        self.startSymbol = ""
        self.firsts = {}
        self.follows = {}

    def prompt(self):
        print("A tool for building LL(1) parse tables based on a grammar defined by the user.")
        print("Enter productions of the form 'S -> xA' where x is a terminal and A is a nonterminal")
        print("The start symbol of the grammar will be set to the nonterminal on the lhs of the first production entered.") 
        self.buildGrammar()    

    def addRule(self, rule):
        try:
            [nonterm,rhs] = [r.strip() for r in rule.split("->")]
            
            # test input is in proper form
            if nonterm.islower():
                print("Nonterminal on left hand side of rule must be uppercase.")
                return
            if len(nonterm) != 1:
                print("Nonterminal must be one uppercase character.")
                return

            # set start symbol if first production entered
            if not self.grammar:
                self.startSymbol = nonterm
             
            # adds new terminals to list of terminals 
            for char in rhs:
                if (char.islower() or not char.isalpha) and char not in self.terminals:
                    self.terminals.append(char)

            # adds rule to grammar
            if nonterm in self.grammar:
                self.grammar[nonterm].append(rhs)
            else:
                self.grammar[nonterm] = [rhs]  
          
        except ValueError:
            print("Error: Rule entered in improper format")
            print("'{0}' should be of the form {1}".format(rule, "S -> A"))

    def buildGrammar(self):
        ruleInput = input("> ").strip()
        while ruleInput != 'e':
            self.addRule(ruleInput)
            ruleInput = input("> ").strip()

        for key in self.grammar.keys():
            self.firsts[key] = "" 
            self.follows[key] = ""

        return self

    def buildParseTable(self):
        pass

    # nonterminal -> ["production", "production"]
    def first(self, productions):
        """Accepts a list of strings, treats each string as a production and compiles a new string that holds all of the possible terminal characters. Returns empty string if not non nullable."""
        # if list is empty, [""] will return true, catch epsilon later
        if not productions:
            # dunno if null or empty string - being optimistic and returning "", relies on logic of caller
            return ""
        else:
            firsts = ""
            for prod in productions:
                if not prod:
                    print("you missed the epsilon")
                for c in prod:
                    # if c is terminal then return c
                    if c in self.terminals:
                        firsts += c
                        # stop looping through single production, move onto next production if exists
                        break
                    # c is nonterminal, as for first of c
                    elif c in self.grammar.keys():
                        # if nothing returned, move on to next one
                        f = self.first(self.grammar[c])
                        # if terminal returned, don't look at next terminals/nonterminals
                        if f:
                            firsts += f
                            break
                        # else continue, check for c as next char in string
                    else:
                        print("error, character {0} not found as terminal or nonterminal\n".format(c), file=sys.stderr)
                        sys.exit(-1)
            return firsts

    def follows(self, nonterm):
        followset = []
        if nonterm == self.startSymbol:
            followset.append("$")

        # walk through all nonterms
        for (key,rules) in self.grammar.items():
            # walk through all rules in current nonterm
            for prod in rules:
                for i,char in enumerate(prod[:-1]):
                    if char.isupper():
                        pass                       
  
    def isNullable(self, t):
        if t not in self.grammar:
            return False
        
        isTermNullable = False 
        # walk through all productions for nonterm 't'
        for i,prod in enumerate(self.grammar[t]):
            isProdNull = True 
            # if prod is epsilon, nullable
            if prod != '':
                for term in prod:
                    if term != t:
                        isProdNull = isProdNull and self.isNullable(term)
                    else: 
                        isProdNull = isProdNull and reduce(lambda x,y: x and y, map(self.isNullable, filter(lambda x: x != term, self.grammar[t])),True)
            isTermNullable = isTermNullable or isProdNull
        return isTermNullable
                

    def __str__(self):
        rules = []
        for (key,val) in self.grammar.items():
            rule = key + " -> " + ' | '.join(self.grammar[key])
            rules.append(rule)
        return "Grammar\n   {0}".format("\n   ".join(rules))         
         

if __name__ == '__main__':
    g = Grammar()
    if len(sys.argv[1:]):
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
            for line in lines: 
                g.addRule(line.strip())
    else:             
        g.prompt()    

    # test follows
    print("grammar ", g.grammar)
    print("terminals  ", g.terminals)
    for term in g.grammar.keys():
        print("IsNullable({0}) = ".format(term), g.isNullable(term))
        print("first({0}) = ".format(term), g.first(g.grammar[term]))

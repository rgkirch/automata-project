from collections import OrderedDict
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
        #self.terminals = []
        self.parseTable = {}
        self.startSymbol = ""
        self.firsts = {}
        self.follows = {}

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

    # nonterminal -> ["production", "production"]
    def first(self, productions):
        """Accepts a list of strings, treats each string as a production and compiles a new string that holds all of the possible terminal characters. Returns empty string if nullable."""
        # if list is empty, [""] will return true, catch epsilon later
        if not productions:
            # dunno if null or empty string - being optimistic and returning "", relies on logic of caller
            return ""
        else:
            firsts = ""
            for prod in productions:
                # won't run on "" epsilon empty string
                for c in prod:
                    print("char",c)
                    # if c is terminal then return c
                    if c in self.terminals:
                        firsts.append(c)
                    # c is nonterminal, as for first of c
                    elif c in self.rules.keys():
                        first.append(self.first(self.rules[c]))
                        # else continue, check for c as next char in string
                    else:
                        print("error, character {0} not found as terminal or nonterminal\n".format(c), file=sys.stderr)
            return firsts

    def follows(self, nonterm):
        pass
 
    def __str__(self):
        rules = []
        for (key,val) in self.grammar.items():
            rule = key + " -> " + ' | '.join(self.grammar[key])
            rules.append(rule)
        return "Grammar\n   {0}".format("\n   ".join(rules))         
         
def prompt():
    print("A tool for building LL(1) parse tables based on a grammar defined by the user.")
    print("Enter productions of the form 'S -> xA' where x is a terminal and A is a nonterminal")
    print("The start symbol of the grammar will be set to the nonterminal on the lhs of the first production entered.") 

if __name__ == '__main__':
    prompt()   
    g = Grammar().buildGrammar()    
    print(g)
    
    

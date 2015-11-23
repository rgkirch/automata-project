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
        self.firstsets = {}
        self.followsets = {}

    def prompt(self):
        print("A tool for building LL(1) parse tables based on a grammar defined by the user.")
        print("Enter productions of the form 'S -> xA' where x is a terminal and A is a nonterminal")
        print("The start symbol of the grammar will be set to the nonterminal on the lhs of the first production entered.") 

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
                if rhs[-1] != '$':
                    print("First rule must end with a '$'")
                    return
             
            # adds new terminals to list of terminals 
            for char in rhs:
                if (char.islower() or not char.isalpha()) and char not in self.terminals:
                    self.terminals.append(char)

            # adds rule to grammar
            if nonterm in self.grammar:
                self.grammar[nonterm].append(rhs)
            else:
                self.grammar[nonterm] = [rhs]  
          
        except ValueError:
            print("Error: Rule entered in improper format")
            print("'{0}' should be of the form {1}".format(rule, "S -> A"))

    def buildGrammar(self, infile=None):
        if infile:
            for line in infile.readlines():
                 self.addRule(line.strip())
        else:
            ruleInput = input("> ").strip()
            while ruleInput != 'e':
                self.addRule(ruleInput)
                ruleInput = input("> ").strip()

        for key in self.grammar.keys():
            self.firstsets[key] = self.first(key) 
            self.followsets[key] = set()

        self.follows()               
 
        return self

    def buildParseTable(self):
        for (nonterminal,production) in self.grammar.items():
            for terminal in self.first(nonterminal):
                try:
                    self.parseTable[nonterminal]
                    try: 
                        self.parseTable[nonterminal][terminal]
                        print("conflict in parse table")
                        sys.exit(-1)
                    except KeyError:
                        self.parseTable[nonterminal][terminal] = self.grammar[nonterminal]
                except KeyError:
                    self.parseTable[nonterminal] = dict()
                    self.parseTable[nonterminal][terminal] = self.grammar[nonterminal]


    # nonterminal -> ["production", "production"]
    def first(self, var):
        """Accepts a list of strings, treats each string as a production and \\
           compiles a new string that holds all of the possible terminal \\
           characters. Returns empty string if not non nullable."""
        firstset = set()
        for prod in self.grammar[var]: 
            for term in prod:
                if self.isNullable(term):
                    firstset.update(self.first(term))
                else:
		    # if term is terminal then add term to
                    # firstset and go to new production
                    if term in self.terminals:
                        firstset.add(term)
                    else:
                        firstset.update(self.first(term))
                    break
        #if var not in self.terminals:
        #    self.firstsets[var] = firstset
        return firstset      

    def firstOfProduction(self, production):
        """Works on right hand side of production."""
        firstset = set()
        for term in prod:
            if self.isNullable(term):
                firstset.update(self.first(term))
            else:
                # if term is terminal then add term to
                # firstset and go to new production
                if term in self.terminals:
                    firstset.add(term)
                else:
                    firstset.update(self.first(term))
                break
        return firstset      
 
    def follows(self):
        self.followsets[self.startSymbol].add("$")
        while True:
            currfollows = dict(self.followsets)
            # walk through all nonterms
            for (key,rules) in self.grammar.items():
		# walk through all rules in current nonterm
                for prod in rules:
                    if prod == '':
                        continue
                    for i,char in enumerate(prod[:-1]):
			# if char is nonterminal
                        if char in self.grammar:
			    # if next char is terminal, add to follows
                            if prod[i+1] in self.terminals:
                                self.followsets[char].add(prod[i+1])
			    # else next char is nonterminal
                            else:
                                if self.isNullable(prod[i+1]):
                                    if prod[i+1] == prod[-1]:
                                        self.followsets[char].update(self.followsets[key])
                                self.followsets[char].update(self.firstsets[prod[i+1]])
			    
                    if prod[-1] in self.grammar.keys():
                        self.followsets[prod[-1]].update(self.firstsets[key])
            # if no changes were made, break out of loop
            if currfollows == self.followsets:
                break
   
    def isNullable(self, var):
        if var in self.terminals:
            return False
        
        isTermNullable = False 
        # walk through all productions for nonterm 'var'
        for i,prod in enumerate(self.grammar[var]):
            isProdNull = True 
            # if prod is epsilon, nullable
            if prod != '':
                for term in prod:
                    if term != var:
                        isProdNull = isProdNull and self.isNullable(term)
                    else: 
                        isProdNull = isProdNull and reduce(lambda x,y: x and y, map(self.isNullable, filter(lambda x: x != term, self.grammar[var])),True)
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
            g.buildGrammar(f)
            g.buildParseTable()
    else:             
        g.prompt()
        g.buildGrammar()
        g.buildParseTable()

    # test follows
    #print("grammar ", g.grammar)
    print("Terminals  ", g.terminals)
    for term in g.grammar.keys():
        print(term, "->", g.grammar[term])
        print("First({0}) = ".format(term), g.first(term))
        print("Parsetable =", g.parseTable[term])
        print("Follows({0}) = ".format(term), g.followsets[term])
        print("IsNullable({0}) = ".format(term), g.isNullable(term))

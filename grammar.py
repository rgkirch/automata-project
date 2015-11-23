from collections import OrderedDict
from functools import reduce
import sys
import stacktrace
import copy

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
    
    def printParseTable(self):
        print("parseTable")
        print("\t", end="")
        for term in self.terminals:
            print(term, "\t", end="")
        print()
        for nonterm in self.grammar.keys():
            print(nonterm, end="")
            for term in self.terminals:
                try:
                    print("\t", self.parseTable[nonterm][term] if self.parseTable[nonterm][term] != "" else "eps", end="")
                except KeyError:
                    print("\t", end="")
            print()

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
            rhs = rhs.strip("$")
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
        for (nonterminal,prod_list) in self.grammar.items():
            # for each production in the grammar
            for prod in prod_list:
                # for each terminal in the first of the right hand side
                for terminal in self.firstOfProduction(prod):
                    self.parseTableAddEntry(nonterminal, terminal, prod)
                # if prod is nullable
                if all(map(self.isNullable, prod)):
                    for f in self.followsets[nonterminal]:
                        self.parseTableAddEntry(nonterminal, f, prod)
                    if "$" in self.followsets[nonterminal]:
                        self.parseTableAddEntry(nonterminal, "$", prod)

    def parseTableAddEntry(self, nonterminal, terminal, prod):
        try:
            self.parseTable[nonterminal]
            try: 
                if self.parseTable[nonterminal][terminal] != prod:
                    print("conflict in parse table when adding")
                    print("nonterm", nonterminal, "terminal", terminal, "production", prod)
                    print(self.parseTable)
                    sys.exit(-1)
            except KeyError:
                self.parseTable[nonterminal][terminal] = prod
        except KeyError:
            self.parseTable[nonterminal] = dict()
            self.parseTable[nonterminal][terminal] = prod


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
        return firstset      

    def firstOfProduction(self, prod):
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
            currfollows = copy.deepcopy(self.followsets)
            # walk through all nonterms
            for (key,rules) in self.grammar.items():
		# walk through all rules in current nonterm
                for prod in rules:
                    print("Checking production '{0}'".format(prod))
                    if prod == '':
                        continue
                    lenProd = len(prod)
                    for i,char in enumerate(prod[:-1]):
			# if char is nonterminal
                        print("   Looking @ char '{0}'".format(char))
                        if char in self.grammar:
                            curr = i+1
                            while curr < lenProd:
                                if self.isNullable(prod[curr]):
                                    print("      {0} is nullable".format(prod[curr]))
                                    if char == prod[-2]:
                                        self.followsets[char].update(self.followsets[key])
                                    print("       adding firstset {0} and follows {1}".format(self.firstsets[prod[curr]], self.followsets[prod[curr]]))
                                    self.followsets[char].update(self.followsets[prod[curr]])
                                    self.followsets[char].update(self.firstsets[prod[curr]])
                                else:
                                    # if next sym is nonnullable nonterminal
                                    if prod[curr] in self.grammar:
                                        # add firstset to current symbols follow set
                                        self.followsets[char].update(self.firstsets[prod[curr]])
                                    else:
                                        # else if its a terminal, simply add to follows
                                        self.followsets[char].add(prod[curr])
                                    break                                                     
                                curr += 1                
  
                    if prod[-1] in self.grammar:
                        self.followsets[prod[-1]].update(self.followsets[key])
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
            inputstring = input("Enter a string to check (empty string to quit): ")
            while inputstring:
                trace = stacktrace.run_stacktrace(g, inputstring)
                stacktrace.printtrace(trace, 0)
                inputstring = input("Enter a string to check (empty string to quit): ")
    else:             
        g.prompt()
        g.buildGrammar()
        g.buildParseTable()

    # test follows
    #print("grammar ", g.grammar)
    print("Terminals  ", g.terminals)
    for term in g.grammar.keys():
        print(term, "->", g.grammar[term])
        print("First({0}) = ".format(term), g.firstsets[term])
        print("Parsetable =", g.parseTable[term])
        print("Follows({0}) = ".format(term), g.followsets[term])
        print("IsNullable({0}) = ".format(term), g.isNullable(term))
        print()
    g.printParseTable()

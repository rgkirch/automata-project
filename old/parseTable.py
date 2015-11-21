import sys
class Grammar():
    terminals = ["+*$"]
    rules = \
    {
        "S":["E$"],
        "A":["+TA"],
        "E":["TA"],
        "B":["*FB"],
        "T":["FB"],
        "F":["(E)", "x"]
    }
    def first(self, productions):
        # if epsilon, return false so parent frame moves on to next character(terminal/nonterminal)
        if not productions:
            # dunno if null or empty string - being optimistic and returning "", relies on logic of caller
            return ""
        else:
            firsts = ""
            for prod in productions:
                for c in prod:
                    print("char",c)
                    # if c is terminal then return c
                    if c in self.terminals:
                        firsts.append(c)
                    # c is nonterminal, as for first of c
                    elif c in self.rules.keys():
                        f = self.first(gram.rules[c])
                        if f:
                            firsts.append(f)
                        # else continue, check for c as next char in string
                    else:
                        print("error, character {0} not found as terminal or nonterminal\n".format(c), file=sys.stderr)
                else:
                    return ""

gram = Grammar()
print(gram.first(gram.rules["S"]))

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
                # won't run on "" epsilon empty string
                for c in prod:
                    # if c is terminal then return c
                    if c in self.terminals:
                        firsts += c
                        # stop looping through single production, move onto next production if exists
                        break
                    # c is nonterminal, as for first of c
                    elif c in self.rules.keys():
                        # if nothing returned, move on to next one
                        f = self.first(self.rules[c])
                        # if terminal returned, don't look at next terminals/nonterminals
                        if f:
                            firsts += f
                            break
                        # else continue, check for c as next char in string
                    else:
                        print("error, character {0} not found as terminal or nonterminal\n".format(c), file=sys.stderr)
                        sys.exit(-1)
            return firsts

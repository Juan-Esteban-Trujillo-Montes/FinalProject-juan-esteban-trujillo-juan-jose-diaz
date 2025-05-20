from First_Follow import compute_first, compute_follow
    
def makeItems(grammar):
    newGrammar = {}
    start_symbol = list(grammar.keys())[0]
    newGrammar["S'"] = [[start_symbol]]
    
    for NonTerm in sorted(grammar.keys()):
        newGrammar[NonTerm] = grammar[NonTerm]

    items = set()
    ordered_keys = ["S'"] + [k for k in sorted(newGrammar.keys()) if k != "S'"]
    for lhs in ordered_keys:
        productions = newGrammar[lhs]
        for prod in productions:
            rhs = list(prod)
            if rhs == ['e']:
                rhs = []
            for dot_pos in range(len(rhs) + 1):
                item_rhs = rhs[:dot_pos] + ['.'] + rhs[dot_pos:]
                items.add((lhs, tuple(item_rhs)))

    return items, newGrammar

def closure(items, newGrammar):
    closure_set = set(items)
    while True:
        new_items = set()
        for (lhs, rhs) in closure_set:
            rhs = list(rhs)
            if '.' in rhs:
                dot_pos = rhs.index('.')

                if dot_pos + 1 < len(rhs):
                    symbol_after_dot = rhs[dot_pos + 1]
                    if symbol_after_dot in newGrammar:
                        for prod in sorted(newGrammar[symbol_after_dot]):
                            if prod == ['e']:
                                prod = []
                            new_item = (symbol_after_dot, tuple(['.'] + list(prod)))
                            if new_item not in closure_set:
                                new_items.add(new_item)
                                
        if not new_items:
            break
        closure_set.update(new_items)

    return closure_set

def goto(items,symbol,newGrammar):
    goto_set = set()
    for (lhs, rhs) in items:
        rhs = list(rhs)
        if '.' in rhs:
            dot_pos = rhs.index('.')
            if dot_pos + 1 < len(rhs) and rhs[dot_pos + 1] == symbol:
                new_rhs = rhs[:dot_pos] + [symbol, '.'] + rhs[dot_pos + 2:]
                goto_set.add((lhs, tuple(new_rhs)))

    return closure(goto_set, newGrammar)

def build_LR0_states(newGrammar):
    start_prod = newGrammar["S'"][0]
    start_item = ("S'", tuple(['.'] + list(start_prod)))
    start_closure = closure([start_item], newGrammar)
    states = [start_closure]
    transitions = {}
    symbols = set()

    for prods in newGrammar.values():
        for prod in prods:
            symbols.update(prod)
    symbols.update(newGrammar.keys())
    symbols = sorted(symbols)

    while True:
        added = False
        for i, state in enumerate(states):
            for symbol in symbols:
                goto_state = goto(state, symbol, newGrammar)
                if goto_state and goto_state not in states:
                    states.append(goto_state)
                    transitions[(i, symbol)] = len(states) - 1
                    added = True
                elif goto_state and goto_state in states:
                    transitions[(i, symbol)] = states.index(goto_state)
        if not added:
            break
    
    return states, transitions

def createSLRtable(states, transitions, newGrammar):
    follow = compute_follow(newGrammar, compute_first(newGrammar))
    action = {}
    goto_table = {}

    productions = []

    is_SLR = True

    conflicts = []

    for NonTerm in sorted(newGrammar.keys()):
        for prod in sorted(newGrammar[NonTerm]):
            if prod == ['e']:
                productions.append((NonTerm, ()))
            else:
                productions.append((NonTerm, tuple(prod)))

    for i, state in enumerate(states): 
        
        for item in sorted(state):
            lhs, rhs = item
            rhs = list(rhs)
            if '.' in rhs:
                dot_pos = rhs.index('.')
                if dot_pos + 1 < len(rhs):
                    symbol = rhs[dot_pos + 1]
                    if symbol not in newGrammar:
                        if (i, symbol) in transitions:
                            key = (i, symbol)
                            new_action = ("shift", transitions[(i, symbol)])
                            if key in action and action[key] != new_action:
                                is_SLR = False
                                conflicts.append((i, symbol, action[key], new_action))
                            action[key] = new_action

                elif dot_pos == len(rhs) - 1:
                    if lhs == "S'":
                        key = (i, '$')
                        new_action = ("accept",)
                        if key in action and action[key] != new_action:
                            is_SLR = False
                            conflicts.append((i, '$', action[key], new_action))
                        action[key] = new_action
                    else:
                        for term in sorted(follow[lhs]):
                            key = (i, term)
                            if rhs[:-1] == []:
                                prod_index = productions.index((lhs, ()))
                            else:
                                prod_index = productions.index((lhs, tuple(rhs[:-1])))
                            new_action = ("reduce", prod_index)
                            if key in action and action[key] != new_action:
                                is_SLR = False
                                conflicts.append((i, term, action[key], new_action))
                            action[key] = new_action

        for symbol in sorted(newGrammar.keys()):
            if (i, symbol) in transitions:
                goto_table[(i, symbol)] = transitions[(i, symbol)]
    

    # Al final de la función, imprime los conflictos si existen
    if not is_SLR:
        for conflict in conflicts:
            i, symbol, prev, new = conflict
            print(f"The grammar is not SLR(1) due to conflict in SLR Table: State {i}, symbol '{symbol}': conflict between {prev} and {new}")
        return False, None, None
    
    else:
        return True, action, goto_table
    
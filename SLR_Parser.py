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
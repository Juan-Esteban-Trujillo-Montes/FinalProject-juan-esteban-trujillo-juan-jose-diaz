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
    

def print_SLR_table(action, goto_table, states, newGrammar):
    # Construir la lista de producciones en orden fijo
    productions = []
    for NonTerm in sorted(newGrammar.keys()):
        for prod in sorted(newGrammar[NonTerm]):
            productions.append((NonTerm, tuple(prod)))

    # Terminales: los que aparecen en action y NO son 'e'
    terminals = set()
    for (_, symbol) in action:
        if symbol != 'e':
            terminals.add(symbol)
    terminals = sorted(terminals)
    # No terminales: los que aparecen en newGrammar (orden fijo)
    non_terminals = sorted(newGrammar.keys())
    if "S'" in non_terminals:
        non_terminals.remove("S'")

    # Encabezado de la tabla unificada
    header = ["State"] + terminals + non_terminals
    print("\nSLR(1) Parsing Table (ACTION & GOTO unificadas):")
    print(" | ".join(f"{h:^12}" for h in header))
    print("-" * (15 * len(header)))

    for i in range(len(states)):
        row = [f"{i:^12}"]
        # ACTION (terminales)
        for t in terminals:
            val = action.get((i, t), "")
            if val:
                if val[0] == "shift":
                    cell = f"s{val[1]}"
                elif val[0] == "reduce":
                    prod = productions[val[1]]
                    # Enumerar desde 1 y mostrar ε si la producción es vacía
                    cell = f"r{val[1]+1}:{prod[0]}→{''.join(prod[1]) if prod[1] else 'ε'}"
                elif val[0] == "accept":
                    cell = "acc"
                else:
                    cell = str(val)
            else:
                cell = ""
            row.append(f"{cell:^12}")
        # GOTO (no terminales)
        for nt in non_terminals:
            val = goto_table.get((i, nt), "")
            row.append(f"{str(val):^12}" if val != "" else " " * 12)
        print(" | ".join(row))

def StringAnalysisSLR(string, action, goto_table, states, newGrammar):
    input_String = list(string) + ['$']
    stack = [0]
    pointer = 0

    productions = []
    for NonTerm in sorted(newGrammar.keys()):
        for prod in sorted(newGrammar[NonTerm]):
            productions.append((NonTerm, tuple(prod)))

    print(f"{'String to analyze: ' + string:^88}")
    print(f"{'Stack':^30} | {'Remaining String':^20} | {'Action':^25}")
    print('-' * 80)

    while True:
        stack_str = str(stack)
        input_str = ''.join(input_String[pointer:])

        state = stack[-1]
        symbol = input_String[pointer]
        action_entry = action.get((state, symbol), None)
        action_entry_str = str(action_entry)

        print(f"{stack_str:^30} | {input_str:^20} | {action_entry_str:25}")

        if action_entry is None:
            print(f"{'String rejected, action not found.\n':^88}")
            return False
        
        if action_entry[0] == "shift":
            stack.append(symbol)
            stack.append(action_entry[1])
            pointer += 1

        elif action_entry[0] == "reduce":
            prod_index = action_entry[1]
            lhs, rhs = productions[prod_index]
            if rhs != () and rhs != ('e',):
                for _ in range(len(rhs) * 2):
                    stack.pop()
            state = stack[-1]
            stack.append(lhs)
            goto_state = goto_table.get((state, lhs), None)

            if goto_state is None:
                print(f"{'String rejected, GOTO state not found\n.':^88}")
                return False
            stack.append(goto_state)
            #print(f"Reducing by production: {lhs} -> {''.join(rhs) if rhs else 'ε'}")

        elif action_entry[0] == "accept":
            print(f"{'String accepted.\n':^88}")
            return True
        else:
            print(f"{'String rejected, invalid action.\n':^88}")
            return False
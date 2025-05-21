from First_Follow import compute_first, compute_follow

# ANSI color and emoji codes for pretty printing
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

def makeItems(grammar):
    # Create an augmented grammar with S' as the new start symbol
    newGrammar = {}
    start_symbol = list(grammar.keys())[0]
    newGrammar["S'"] = [[start_symbol]]

    # Copy the original grammar productions, sorted by non-terminal
    for NonTerm in sorted(grammar.keys()):
        newGrammar[NonTerm] = grammar[NonTerm]

    # Build the set of LR(0) items
    items = set()
    ordered_keys = ["S'"] + [k for k in sorted(newGrammar.keys()) if k != "S'"]
    for lhs in ordered_keys:
        productions = newGrammar[lhs]
        for prod in productions:
            rhs = list(prod)
            if rhs == ['e']:
                rhs = []  # Treat epsilon as an empty production
            # Insert the dot at each position in the production
            for dot_pos in range(len(rhs) + 1):
                item_rhs = rhs[:dot_pos] + ['.'] + rhs[dot_pos:]
                items.add((lhs, tuple(item_rhs)))

    return items, newGrammar

def closure(items, newGrammar):
    # Compute the closure of a set of LR(0) items.
    closure_set = set(items)
    while True:
        new_items = set()
        for (lhs, rhs) in closure_set:
            rhs = list(rhs)
            if '.' in rhs:
                dot_pos = rhs.index('.')
                # If dot is before a non-terminal, add items for its productions
                if dot_pos + 1 < len(rhs):
                    symbol_after_dot = rhs[dot_pos + 1]
                    if symbol_after_dot in newGrammar:
                        for prod in sorted(newGrammar[symbol_after_dot]):
                            if prod == ['e']:
                                prod = []  # Treat epsilon as an empty production
                            new_item = (symbol_after_dot, tuple(['.'] + list(prod)))
                            if new_item not in closure_set:
                                new_items.add(new_item)
        if not new_items:
            break
        closure_set.update(new_items)
    return closure_set

def goto(items, symbol, newGrammar):
    # Compute the GOTO set after reading 'symbol' from the given set of items.
    goto_set = set()
    for (lhs, rhs) in items:
        rhs = list(rhs)
        if '.' in rhs:
            dot_pos = rhs.index('.')
            # If the dot is followed by the given symbol, move the dot past it
            if dot_pos + 1 < len(rhs) and rhs[dot_pos + 1] == symbol:
                new_rhs = rhs[:dot_pos] + [symbol, '.'] + rhs[dot_pos + 2:]
                goto_set.add((lhs, tuple(new_rhs)))
    # Return the closure of the resulting set
    return closure(goto_set, newGrammar)

def build_LR0_states(newGrammar):
    # Build all LR(0) states and transitions for the grammar
    start_prod = newGrammar["S'"][0]
    start_item = ("S'", tuple(['.'] + list(start_prod)))
    start_closure = closure([start_item], newGrammar)
    states = [start_closure]
    transitions = {}
    symbols = set()

    # Gather all grammar symbols (terminals and non-terminals)
    for prods in newGrammar.values():
        for prod in prods:
            symbols.update(prod)
    symbols.update(newGrammar.keys())
    symbols = sorted(symbols)

    # Build the canonical collection of sets of LR(0) items
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
    # Compute the SLR(1) parsing table (ACTION and GOTO)
    follow = compute_follow(newGrammar, compute_first(newGrammar))
    action = {}
    goto_table = {}

    productions = []
    is_SLR = True
    conflicts = []

    # Build a list of productions for referencing in reductions
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
                # If dot is not at the end, and after dot is a terminal, add shift action
                if dot_pos + 1 < len(rhs):
                    symbol = rhs[dot_pos + 1]
                    if symbol not in newGrammar:
                        if (i, symbol) in transitions:
                            key = (i, symbol)
                            new_action = ("shift", transitions[(i, symbol)])
                            # Detect shift/reduce or shift/shift conflicts
                            if key in action and action[key] != new_action:
                                is_SLR = False
                                conflicts.append((i, symbol, action[key], new_action))
                            action[key] = new_action

                # If dot is at the end, add reduce or accept actions
                elif dot_pos == len(rhs) - 1:
                    if lhs == "S'":
                        key = (i, '$')
                        new_action = ("accept",)
                        # Detect accept/reduce or accept/shift conflicts
                        if key in action and action[key] != new_action:
                            is_SLR = False
                            conflicts.append((i, '$', action[key], new_action))
                        action[key] = new_action
                    else:
                        for term in sorted(follow[lhs]):
                            key = (i, term)
                            # Find the production index for reduction
                            if rhs[:-1] == []:
                                prod_index = productions.index((lhs, ()))
                            else:
                                prod_index = productions.index((lhs, tuple(rhs[:-1])))
                            new_action = ("reduce", prod_index)
                            # Detect reduce/reduce or reduce/shift conflicts
                            if key in action and action[key] != new_action:
                                is_SLR = False
                                conflicts.append((i, term, action[key], new_action))
                            action[key] = new_action

        # Fill the GOTO table for non-terminals
        for symbol in sorted(newGrammar.keys()):
            if (i, symbol) in transitions:
                goto_table[(i, symbol)] = transitions[(i, symbol)]
    
    # At the end, print conflicts if any were found
    if not is_SLR:
        for conflict in conflicts:
            i, symbol, prev, new = conflict
            print(f"{RED}🚫 The grammar is not SLR(1), Conflict in SLR Table: State {i}, symbol '{symbol}': conflict between {prev} and {new}{RESET}")
        return False, None, None
    else:
        return True, action, goto_table

def print_SLR_table(action, goto_table, states, newGrammar):
    # Build the list of all productions for referencing in reductions
    productions = []
    for NonTerm in sorted(newGrammar.keys()):
        for prod in sorted(newGrammar[NonTerm]):
            productions.append((NonTerm, tuple(prod)))

    # Terminals: all symbols in the ACTION table except 'e'
    terminals = set()
    for (_, symbol) in action:
        if symbol != 'e':
            terminals.add(symbol)
    terminals = sorted(terminals)
    # Non-terminals: all grammar non-terminals except S'
    non_terminals = sorted(newGrammar.keys())
    if "S'" in non_terminals:
        non_terminals.remove("S'")

    # Print unified ACTION & GOTO table header
    header = ["State"] + terminals + non_terminals
    print(f"\n{BOLD}{MAGENTA} 📊 SLR(1) Parsing Table (ACTION & GOTO unified):{RESET}")
    print(" | ".join(f"{BOLD}{MAGENTA}{h:^12}{RESET}" for h in header))
    print(f"{CYAN}{"-" * (15 * len(header))}")
    
    # Print each row of the table
    for i in range(len(states)):
        row = [f"{CYAN}{BOLD}{i:^12}{RESET}"]
        # ACTION (terminals)
        for t in terminals:
            val = action.get((i, t), "")
            if val:
                if val[0] == "shift":
                    cell = f"s{val[1]}"
                elif val[0] == "reduce":
                    prod = productions[val[1]]
                    # Show ε for empty production
                    cell = f"r{val[1]+1}:{prod[0]}→{''.join(prod[1]) if prod[1] else 'ε'}"
                elif val[0] == "accept":
                    cell = "acc"
                else:
                    cell = str(val)
            else:
                cell = ""
            row.append(f"{cell:^12}")
        # GOTO (non-terminals)
        for nt in non_terminals:
            val = goto_table.get((i, nt), "")
            row.append(f"{str(val):^12}" if val != "" else " " * 12)
        print(" | ".join(row))

def StringAnalysisSLR(string, action, goto_table, states, newGrammar):
    # Simulate SLR parsing for the given string using the parsing tables
    input_String = list(string) + ['$']
    stack = [0]
    pointer = 0

    # Build the list of all productions for referencing in reductions
    productions = []
    for NonTerm in sorted(newGrammar.keys()):
        for prod in sorted(newGrammar[NonTerm]):
            productions.append((NonTerm, tuple(prod)))

    print(f"{BOLD}{'🔎 String to analyze: ' + string:^85}{RESET}")
    print(f"{MAGENTA}{BOLD}{'Stack':^30}{RESET} | {MAGENTA}{BOLD}{'Remaining String':^20}{RESET} | {MAGENTA}{BOLD}{'Action':^25}{RESET}")
    print(f"{CYAN}{'-' * 80}{RESET}")

    while True:
        stack_str = str(stack)
        input_str = ''.join(input_String[pointer:])

        state = stack[-1]
        symbol = input_String[pointer]
        action_entry = action.get((state, symbol), None)
        action_entry_str = str(action_entry)

        print(f"{stack_str:^30} | {input_str:^20} | {action_entry_str:^25}")

        if action_entry is None:
            print()
            print(f"{RED}{'❌ String rejected, action not found.':^88}\n{RESET}")
            return False
        
        if action_entry[0] == "shift":
            # Push the terminal and the new state onto the stack
            stack.append(symbol)
            stack.append(action_entry[1])
            pointer += 1

        elif action_entry[0] == "reduce":
            prod_index = action_entry[1]
            lhs, rhs = productions[prod_index]
            # Pop stack for each symbol in rhs (2 pops for symbol and state)
            if rhs != () and rhs != ('e',):
                for _ in range(len(rhs) * 2):
                    stack.pop()
            state = stack[-1]
            # Push the non-terminal and the new state after GOTO
            stack.append(lhs)
            goto_state = goto_table.get((state, lhs), None)

            if goto_state is None:
                print()
                print(f"{RED}{'❌ String rejected, GOTO state not found.':^88}\n{RESET}")
                return False
            stack.append(goto_state)

        elif action_entry[0] == "accept":
            print()
            print(f"{GREEN}{'✅ String accepted ✅\n':^88}{RESET}")
            return True
        else:
            print(f"{RED}{'❌ String rejected, invalid action.\n':^88}{RESET}")
            return False
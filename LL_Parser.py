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

def verify_LL1(grammar):
    # Check for immediate left recursion in the grammar
    for nonTerminal, productions in grammar.items():
        for prod in productions:
            if prod[0] == nonTerminal:
                print(f"{RED}🚫 The grammar is not LL(1) due to left recursion in {nonTerminal} -> {''.join(prod)}{RESET}")
                return False

    # Compute FIRST and FOLLOW sets
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)

    # Check pairwise disjointness of FIRST sets (and FIRST/FOLLOW if epsilon present)
    for nonTerminal in grammar:
        productions = grammar[nonTerminal]
        for i in range(len(productions)):
            prod_i = productions[i]
            first_i = set()
            # Calculate FIRST set for production i
            for symbol in prod_i:
                first_i.update(first[symbol]-{'e'})
                if 'e' not in first[symbol]:
                    break
            else:
                first_i.add('e')

            for j in range(i + 1, len(productions)):
                prod_j = productions[j]
                first_j = set()
                # Calculate FIRST set for production j
                for symbol in prod_j:
                    first_j.update(first[symbol]-{'e'})
                    if 'e' not in first[symbol]:
                        break
                else:
                    first_j.add('e')

                # If epsilon in either FIRST set, check intersection with FOLLOW
                if 'e' in first_i:
                    if first_j.intersection(follow[nonTerminal]):
                        print(f"{RED}🚫 Grammar is not LL(1) due to {BOLD}{nonTerminal}{RESET} -> {''.join(prod_i)} and {nonTerminal}{RESET} -> {''.join(prod_j)}{RESET}")
                        return False

                if 'e' in first_j:
                    if first_i.intersection(follow[nonTerminal]):
                        print(f"{RED}🚫 Grammar is not LL(1) due to {BOLD}{nonTerminal}{RESET} -> {''.join(prod_i)} and {nonTerminal}{RESET} -> {''.join(prod_j)}{RESET}")
                        return False

                # If FIRST sets of prod_i and prod_j intersect, not LL(1)
                if first_i.intersection(first_j):
                    print(f"{RED}🚫 Grammar is not LL(1) due to {BOLD}{nonTerminal}{RESET} -> {''.join(prod_i)} and {nonTerminal}{RESET} -> {''.join(prod_j)}{RESET}")
                    return False
    return True

def createTableLL(grammar):
    # Compute FIRST and FOLLOW sets
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)
    table = {}

    # For each non-terminal, initialize its table entries
    for nonTerminal in grammar:
        table[nonTerminal] = {}
        productions = grammar[nonTerminal]

        for production in productions:
            first_set = set()
            # Get FIRST set for this production
            for symbol in production:
                first_set.update(first[symbol]-{'e'})
                if 'e' not in first[symbol]:
                    break
            else:
                first_set.add('e')
            # Fill table for each terminal in FIRST (except epsilon)
            for terminal in first_set-{'e'}:
                if terminal not in table[nonTerminal]:
                    table[nonTerminal][terminal] = production
                else:
                    print(f"{RED}⚠️ Conflict in LL(1) table for {BOLD}{nonTerminal}{RESET} -> {''.join(production)} and {nonTerminal}{RESET} -> {''.join(table[nonTerminal][terminal])}{RESET}")
                    print(f"{RED}Grammar is not LL(1){RESET}")
                    return None
            # If epsilon in FIRST, fill table for each symbol in FOLLOW
            if 'e' in first_set:
                for terminal in follow[nonTerminal]:
                    if terminal not in table[nonTerminal]:
                        table[nonTerminal][terminal] = production
                    else:
                        print(f"{RED}⚠️ Conflict in LL(1) table for {BOLD}{nonTerminal}{RESET} -> {''.join(production)} and {nonTerminal}{RESET} -> {''.join(table[nonTerminal][terminal])}{RESET}")
                        print(f"{RED}Grammar is not LL(1){RESET}")
                        return None

    return table

def print_ll1_table(table):
    # Gather all terminals used in table
    terminals = set()
    for rules in table.values():
        terminals.update(rules.keys())
    terminals = sorted(terminals)

    # Print the table header
    print(f"{BOLD}{MAGENTA}{'':5}{RESET}|", end='')
    for term in terminals:
        print(f"{BOLD}{MAGENTA} {term:^10}{RESET}|", end='')
    print()
    print("-" * (12 * (len(terminals) + 1)))

    # Print each row of the table
    for non_terminal, rules in table.items():
        print(f"{BOLD}{CYAN}{non_terminal:^5}{RESET}|", end='')
        for term in terminals:
            prod = rules.get(term)
            if prod:
                prod_str = f"{non_terminal}→{''.join(prod)}"
            else:
                prod_str = ''
            print(f" {prod_str:^10}|", end='')
        print()

def StringAnalysisLL(string, table):
    # Print the string to be analyzed
    print(f"{BOLD}{'🔎 String to analyze: ' + string:^66}{RESET}")

    stack = ['$','S']  # Initialize stack with end marker and start symbol
    index = 0
    string += '$'      # Append end marker to input string
    
    print(f"{MAGENTA}{BOLD}{'Stack':^30}{RESET} | {MAGENTA}{BOLD}{'Remaining String':^38}{RESET}")
    print(f"{CYAN}{'-' * 72}{RESET}")

    while len(stack) != 1:
        pila_str = ''.join(list(reversed(stack)))
        restante_str = string[index:]
        print(f"{pila_str:^30} | {restante_str:^38}")
        top = stack.pop()            # Pop top symbol from stack
        currentCharacter = string[index]

        if top == currentCharacter:
            index += 1               # Matched terminal, advance in input
            continue

        if top in table and currentCharacter in table[top]:
            production = table[top][currentCharacter]
            if production == ['e']:
                continue             # Epsilon production, nothing to push
            for symbol in reversed(production):
                stack.append(symbol) # Push production symbols to stack (in reverse)
        else:
            print()
            print(f"{RED} {'❌ Error: Unexpected symbol ' + currentCharacter + ' at index ' + str(index):^66}{RESET}")
            print(f"{RED} {'❌ String is rejected ❌':^66}\n{RESET}")
            return False
           
    pila_str = ''.join(list(reversed(stack)))
    restante_str = string[index:]
    print(f"{pila_str:^30} | {restante_str:^38}")

    # Accept if input is fully consumed and only end marker remains on stack
    if string[index] == '$' and stack == ['$']:
        print()
        print(f"{GREEN} {'✅ String is accepted ✅':^58}{RESET}\n")
        return True
    else:
        print()
        print(f"{'String is rejected\n':^62}")
        return False
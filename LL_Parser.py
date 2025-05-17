from First_Follow import compute_first, compute_follow
def verify_LL1(grammar):

    for nonTerminal, productions in grammar.items():
        for prod in productions:
            if prod[0] == nonTerminal:
                print(f"The grammar is not LL(1) due to left recursion in {nonTerminal} -> {prod}")
                return False

    first = compute_first(grammar)
    follow = compute_follow(grammar, first)

    for nonTerminal in grammar:
        productions = grammar[nonTerminal]
        
        for i in range(len(productions)):
            prod_i = productions[i]
            first_i = set()

            for symbol in prod_i:
                first_i.update(first[symbol]-{'e'})
                if 'e' not in first[symbol]:
                    break
            else:
                first_i.add('e')

            for j in range(i + 1, len(productions)):
                prod_j = productions[j]
                first_j = set()

                for symbol in prod_j:
                    first_j.update(first[symbol]-{'e'})
                    if 'e' not in first[symbol]:
                        break
                else:
                    first_j.add('e')

                if 'e' in first_i:
                    if first_j.intersection(follow[nonTerminal]):
                        print(f"Grammar is not LL(1) due to {nonTerminal} -> {prod_i} and {nonTerminal} -> {prod_j}")
                        return False

                if  'e' in first_j:
                    if first_i.intersection(follow[nonTerminal]):
                        print(f"Grammar is not LL(1) due to {nonTerminal} -> {prod_i} and {nonTerminal} -> {prod_j}")
                        return False
                
                if first_i.intersection(first_j):
                    print(f"Grammar is not LL(1) due to {nonTerminal} -> {prod_i} and {nonTerminal} -> {prod_j}")
                    return False
    return True

def createTableLL(grammar):
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)
    table = {}

    for nonTerminal in grammar:
        table[nonTerminal] = {}
        productions = grammar[nonTerminal]

        for production in productions:
            first_set = set()

            for symbol in production:
                first_set.update(first[symbol]-{'e'})
                if 'e' not in first[symbol]:
                    break
            else:
                first_set.add('e')
            
            for terminal in first_set-{'e'}:
                if terminal not in table[nonTerminal]:
                    table[nonTerminal][terminal] = production
                else:
                    print(f"Conflict in LL(1) table for {nonTerminal} -> {production} and {nonTerminal} -> {table[nonTerminal][terminal]}")
                    print("Grammar is not LL(1)")
                    return None
            
            if 'e' in first_set:
                for terminal in follow[nonTerminal]:
                    if terminal not in table[nonTerminal]:
                        table[nonTerminal][terminal] = production
                    else:
                        print(f"Conflict in LL(1) table for {nonTerminal} -> {production} and {nonTerminal} -> {table[nonTerminal][terminal]}")
                        print("Grammar is not LL(1)")
                        return None

    return table

def print_ll1_table(table):
    terminals = set()
    for rules in table.values():
        terminals.update(rules.keys())
    terminals = sorted(terminals)

    print(f"{'':5}|", end='')
    for term in terminals:
        print(f" {term:^10}|", end='')
    print("\n" + "-" * (12 * (len(terminals) + 1)))

    for non_terminal, rules in table.items():
        print(f"{non_terminal:^5}|", end='')
        for term in terminals:
            prod = rules.get(term)
            if prod:
                prod_str = f"{non_terminal}→{''.join(prod)}"
            else:
                prod_str = ''
            print(f" {prod_str:^10}|", end='')
        print()

def StringAnalysisLL(string, table):
    print(f"{'String to analyze: ' + string:^66}")

    stack = ['$','S']
    index = 0
    string += '$'
    
    print(f"{'Stack':^30} | {'Remaining String':^38}")
    print("-" * 72)

    while len(stack) != 1:
        pila_str = ''.join(list(reversed(stack)))
        restante_str = string[index:]
        print(f"{pila_str:^30} | {restante_str:^38}")
        top = stack.pop()
        currentCharacter = string[index]

        if top == currentCharacter:
            index += 1
            continue

        if top in table and currentCharacter in table[top]:
            production = table[top][currentCharacter]

            if production == ['e']:
                continue

            for symbol in reversed(production):
                stack.append(symbol)
        else:
            print()
            print(f"{'Error: Unexpected symbol ' + currentCharacter + ' at index ' + str(index):^66}")
            print(f"{'String is rejected\n':^66}")
            return False
           
    pila_str = ''.join(list(reversed(stack)))
    restante_str = string[index:]
    print(f"{pila_str:^30} | {restante_str:^38}")

    if string[index] == '$' and stack == ['$']:
        print()
        print(f"{'String is accepted\n':^62}")
        return True
    else:
        print()
        print(f"{'String is rejected\n':^62}")
        return False
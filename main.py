from First_Follow import compute_first, compute_follow
from LL_Parser import verify_LL1, createTableLL, print_ll1_table, StringAnalysisLL
from SLR_Parser import makeItems, closure, goto, build_LR0_states, createSLRtable
def ReadGrammars(filename):
    grammars = []
    with open(filename, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = line.strip()
            if line.isdigit():
                n = int(line)
                grammar = {}
                for _ in range(n):
                    line = file.readline().strip()
                    head, body = line.split("->")
                    head = head.strip()
                    productions = body.strip().split()
                    for prod in productions:
                        symbols = list(prod)
                        grammar.setdefault(head, []).append(symbols)
                grammars.append(grammar)
    
    print("¡The grammars are read successfully!\n")
    return grammars

print("Reading grammars from input file...")
input_file = "input.txt"
grammars = ReadGrammars(input_file)

print("Available grammars:")
for grammar in grammars:
    print(f"Grammar {grammars.index(grammar) + 1}:")
    for nonTerminal, productions in grammar.items():
            print(f"{nonTerminal} -> {' | '.join([''.join(prod) for prod in productions])}")
    print()

while True:
    print("Select an option:")
    print("1. Calculate First and Follow sets")
    print("2. Calculate LR(0) items")
    print("3. Build LR(0) states and transitions")
    print("4. Parser Compatibility")

    print("Q. Quit")
    option = input("Enter your choice: ").upper()
    print()

    if option == "1":
        grammar_num = input("Enter the grammar number to calculate First and Follow sets: ")
        if not grammar_num.isdigit() or int(grammar_num) < 1 or int(grammar_num) > len(grammars):
            print("Invalid grammar number. Please try again.\n")
            continue
        grammar = grammars[int(grammar_num) - 1]
        first = compute_first(grammar)
        follow = compute_follow(grammar, first)
        print("First sets:")
        for nonTerminal, firstSet in first.items():
            print(f"First({nonTerminal}) = {{ {', '.join(firstSet)} }}")
        print("\nFollow sets:")
        for nonTerminal, followSet in follow.items():
            print(f"Follow({nonTerminal}) = {{ {', '.join(followSet)} }}")
        print()

    elif option == "2":
        grammar_num = input("Enter the grammar number to calculate items: ")
        if not grammar_num.isdigit() or int(grammar_num) < 1 or int(grammar_num) > len(grammars):
            print("Invalid grammar number. Please try again.\n")
            continue

        grammar = grammars[int(grammar_num) - 1]
        items, new_grammar = makeItems(grammar)
        print("LR(0) Items for the selected grammar:")

        for item in sorted(items):
            lhs, rhs = item
            if lhs == "S'":
                print(f"{lhs} -> {' '.join(rhs) if rhs else 'e'}")
        for item in sorted(items):
            lhs, rhs = item
            if lhs != "S'":
                print(f"{lhs} -> {' '.join(rhs) if rhs else 'e'}")
        print()

    elif option == "3":
        grammar_num = input("Enter the grammar number to print LR(0) states and transitions: ")
        if not grammar_num.isdigit() or int(grammar_num) < 1 or int(grammar_num) > len(grammars):
            print("Invalid grammar number. Please try again.\n")
            continue

        grammar = grammars[int(grammar_num) - 1]
        items, new_grammar = makeItems(grammar)
        states, transitions = build_LR0_states(new_grammar)
        print("\nLR(0) States:")
        for idx, state in enumerate(states):
            print(f"State {idx}:")
            for item in sorted(state):
                lhs, rhs = item
                print(f"  {lhs} -> {' '.join(rhs)}")
            print()
        print("Transitions:")
        for (i, symbol), j in sorted(transitions.items()):
            print(f"  State {i} -- {symbol} --> State {j}")
        print()

    elif option == "4":
        grammar_num = input("Enter the grammar number to check grammar compatibility: ")
        if not grammar_num.isdigit() or int(grammar_num) < 1 or int(grammar_num) > len(grammars):
            print("Invalid grammar number. Please try again.\n")
            continue
        
        grammar = grammars[int(grammar_num) - 1]

        is_LL = verify_LL1(grammar)

        items, new_grammar = makeItems(grammar)
        states, transitions = build_LR0_states(new_grammar)
        is_SLR, action, goto_table = createSLRtable(states, transitions, new_grammar)

        if is_LL and is_SLR:
            while True:
                print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
                option = input("Enter your choice: ").upper()
                if option == "T":
                    table = createTableLL(grammar)
                    print("LL(1) Parsing Table:")
                    print_ll1_table(table)
                    string = input("Enter a string to analyze: ")
                    StringAnalysisLL(string, table)
                    

                elif option == "B":
                   pass
                    
                elif option == "Q":
                    break
                else:
                    print("Invalid option. Please try again.")

        elif is_LL and not is_SLR:
            print("The grammar is LL(1).")
            table = createTableLL(grammar)
            print("LL(1) Parsing Table:")
            print_ll1_table(table)
            string = input("Enter a string to analyze: ")
            StringAnalysisLL(string, table)

        elif not is_LL and is_SLR:
            print("The grammar is SLR(1).")
            
            
        else:
            print("The Grammar is neither LL(1) nor SLR(1).\n")
                
    elif option == "Q":
        exit()

    else:
        print("Invalid option. Please try again.")
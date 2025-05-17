from First_Follow import compute_first, compute_follow
from LL_Parser import verify_LL1, createTableLL, print_ll1_table, StringAnalysisLL
from SLR_Parser import makeItems, closure, goto
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
        if not grammar_num.isdigit() or int(grammar) < 1 or int(grammar) > len(grammars):
            print("Invalid grammar number. Please try again.\n")
            continue
        grammar = grammars[int(grammar) - 1]
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
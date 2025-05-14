from First_Follow import compute_first, compute_follow
from LL_Parser import verify_LL1, createTableLL, print_ll1_table, StringAnalysis

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
    return grammars


if __name__ == "__main__":
    input_file = "input.txt"
    grammars = ReadGrammars(input_file)
    print(grammars)
    for i, grammar in enumerate(grammars):
        print(f"Grammar {i + 1}:")
        for nonTerminal, productions in grammar.items():
            print(f"{nonTerminal} -> {' | '.join([''.join(prod) for prod in productions])}")
        print()

        first = compute_first(grammar)
        print("First sets:")
        for nonTerminal, firstSet in first.items():
            print(f"First({nonTerminal}) = {{ {', '.join(firstSet)} }}")

        follow = compute_follow(grammar, first)
        print("Follow sets:")
        for nonTerminal, followSet in follow.items():
            print(f"Follow({nonTerminal}) = {{ {', '.join(followSet)} }}")
        print()

        print("Verifying if the grammar is LL(1)...")
        verify_LL1(grammar)

        print()

        table = createTableLL(grammar)
        if table is not None:
            print_ll1_table(table)
        else:
            print("The table parsing cannot be created because the grammar is not LL(1).")
            print()
            continue

        print()

        tested_string = "ad"
        StringAnalysis(tested_string, table)

        print()
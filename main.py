from First_Follow import compute_first, compute_follow
from LL_Parser import verify_LL1, createTableLL, print_ll1_table, StringAnalysisLL
from SLR_Parser import makeItems, closure, goto, build_LR0_states, createSLRtable, print_SLR_table, StringAnalysisSLR

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

def ReadGrammars(filename):
    # Reads grammars from a file, each grammar is specified by the number of rules followed by the rules.
    grammars = []
    with open(filename, "r") as file:
        while True:
            line = file.readline() # Read a line from the file
            if not line:
                break  # Stop if end of file
            line = line.strip()
            if line.isdigit():
                n = int(line)  # Number of productions for this grammar
                grammar = {}
                for _ in range(n):
                    line = file.readline().strip()
                    head, body = line.split("->")  # Split into LHS and RHS
                    head = head.strip()
                    productions = body.strip().split()  # Productions separated by whitespace
                    for prod in productions:
                        symbols = list(prod)   # Each production as a list of symbols
                        grammar.setdefault(head, []).append(symbols)
                grammars.append(grammar)  # Add grammar to the list

    print(f"{GREEN}✅ {BOLD}The grammars are read successfully!{RESET}\n")
    return grammars

def colorize_production(prod, color=CYAN):
    return f"{color}{''.join(prod)}{RESET}"

def separator():
    print(f"{MAGENTA}{'═'*120}{RESET}")

# Start of the program
print(f"{BLUE}{BOLD}📚 Reading grammars from input file...{RESET}")
input_file = "input.txt"
grammars = ReadGrammars(input_file)

# Print all grammars read from the file
print(f"\n{MAGENTA}{BOLD}✨ Available grammars:{RESET}")
for idx, grammar in enumerate(grammars):
    print(f"{BOLD}{CYAN}Grammar {idx + 1}:{RESET}")
    for nonTerminal, productions in grammar.items():
        # Print each production in the grammar
        prods_str = f"{' | '.join([''.join(prod) for prod in productions])}"
        print(f"  {GREEN}{nonTerminal}{RESET} {YELLOW}->{RESET} {prods_str}")
    print()

# Main interaction loop
while True:
    separator()
    print(f"{YELLOW}{BOLD}🌟 Select an option:{RESET}")
    print(f"{CYAN}1.{RESET}📋 Calculate First and Follow sets")
    print(f"{CYAN}2.{RESET}🧩 Calculate LR(0) items")
    print(f"{CYAN}3.{RESET}🧮 Build LR(0) states and transitions")
    print(f"{CYAN}4.{RESET}🤖 Parser Compatibility")
    print(f"{RED}Q.{RESET} ❌ Quit")
    option = input(f"{BOLD}Enter your choice:{RESET} ").upper()
    print()

    if option == "1":
        # Calculate and display FIRST and FOLLOW sets
        grammar_num = input(f"{BOLD}🔢 Enter the grammar number to calculate First and Follow sets:{RESET} ")

        if not grammar_num.isdigit() or int(grammar_num) < 1 or int(grammar_num) > len(grammars):
            print(f"{RED}🚫 Invalid grammar number. Please try again.{RESET}\n")
            continue

        grammar = grammars[int(grammar_num) - 1]
        first = compute_first(grammar)
        follow = compute_follow(grammar, first)

        print(f"{BOLD}{MAGENTA}🟢 First sets:{RESET}")
        for nonTerminal, firstSet in first.items():
            print(f"  {CYAN}First({GREEN}{nonTerminal}{CYAN}){RESET} = {{ {', '.join(sorted(firstSet))} }}")
        
        print(f"\n{BOLD}{MAGENTA}🔵 Follow sets:{RESET}")
        for nonTerminal, followSet in follow.items():
            print(f"  {CYAN}Follow({GREEN}{nonTerminal}{CYAN}){RESET} = {{ {', '.join(sorted(followSet))} }}")
        print()

    elif option == "2":
        # Calculate and display LR(0) items
        grammar_num = input(f"{BOLD}🔢 Enter the grammar number to calculate items:{RESET} ")

        if not grammar_num.isdigit() or int(grammar_num) < 1 or int(grammar_num) > len(grammars):
            print(f"{RED}🚫 Invalid grammar number. Please try again.{RESET}\n")
            continue

        grammar = grammars[int(grammar_num) - 1]
        items, new_grammar = makeItems(grammar)

        print(f"{BOLD}{YELLOW}🧩 LR(0) Items for the selected grammar:{RESET}")

        # Print items where the LHS is the augmented start symbol first
        for item in sorted(items):
            lhs, rhs = item
            if lhs == "S'":
                color = GREEN
                print(f"{BOLD}{color}{lhs}{RESET} {YELLOW}->{RESET} {' '.join(rhs) if rhs else 'e'}")
        
         # Print all other items
        for item in sorted(items):
            lhs, rhs = item
            if lhs != "S'":
                print(f"{BOLD}{CYAN}{lhs}{RESET} {YELLOW}->{RESET} {' '.join(rhs) if rhs else 'e'}")
        print()

    elif option == "3":
        # Calculate and display LR(0) states and transitions
        grammar_num = input(f"{BOLD}🔢 Enter the grammar number to print LR(0) states and transitions:{RESET} ")
        if not grammar_num.isdigit() or int(grammar_num) < 1 or int(grammar_num) > len(grammars):
            print(f"{RED}🚫 Invalid grammar number. Please try again.{RESET}\n")
            continue

        grammar = grammars[int(grammar_num) - 1]
        items, new_grammar = makeItems(grammar)
        states, transitions = build_LR0_states(new_grammar)

        print(f"\n{BOLD}{MAGENTA}🏁 LR(0) States:{RESET}")
        for idx, state in enumerate(states):
            print(f"{BOLD}{YELLOW}State {idx}:{RESET}")
            for item in sorted(state):
                lhs, rhs = item
                print(f"  {BOLD}{CYAN}{lhs}{RESET} {YELLOW}->{RESET} {' '.join(rhs)}")
            print()
        
        print(f"{BOLD}{CYAN}🔀 Transitions:{RESET}")
        for (i, symbol), j in sorted(transitions.items()):
            print(f"  State {i} {YELLOW}--{RESET} {symbol} {YELLOW}-->{RESET} State {j}")
        print()

    elif option == "4":
        # Analyze parser compatibility: LL(1), SLR(1), or neither
        grammar_num = input(f"{BOLD}🔢 Enter the grammar number to check grammar compatibility:{RESET} ")
        if not grammar_num.isdigit() or int(grammar_num) < 1 or int(grammar_num) > len(grammars):
            print(f"{RED}🚫 Invalid grammar number. Please try again.{RESET}\n")
            continue
        
        grammar = grammars[int(grammar_num) - 1]

        # Check LL(1) compatibility
        is_LL = verify_LL1(grammar)

        # Build LR(0) structures for SLR(1) analysis
        items, new_grammar = makeItems(grammar)
        states, transitions = build_LR0_states(new_grammar)
        is_SLR, action, goto_table = createSLRtable(states, transitions, new_grammar)

        if is_LL and is_SLR:
            # If grammar is both LL(1) and SLR(1), offer both parsing methods
            print(f"{GREEN}🎉 The grammar is both LL(1) and SLR(1)!{RESET}")
            while True:
                print(f"{YELLOW}🤔 Select a parser ({CYAN}T{YELLOW}: for LL(1), {CYAN}B{YELLOW}: for SLR(1), {RED}Q{YELLOW}: quit):{RESET}")
                option = input(f"{BOLD}Enter your choice:{RESET} ").upper()

                if option == "T":
                    table = createTableLL(grammar)
                    print(f"{BOLD}{MAGENTA}📊 LL(1) Parsing Table:{RESET}")
                    print_ll1_table(table)
                    string = input(f"{BOLD}✍️  Enter a string to analyze:{RESET} ")
                    StringAnalysisLL(string, table)

                elif option == "B":
                    print_SLR_table(action, goto_table, states, new_grammar)
                    string = input(f"{BOLD}✍️  Enter a string to analyze:{RESET} ")
                    StringAnalysisSLR(string, action, goto_table, states, new_grammar)

                elif option == "Q":
                    break

                else:
                    print(f"{RED}🚫 Invalid option. Please try again.{RESET}")

        elif is_LL and not is_SLR:
            # If only LL(1)
            print(f"{GREEN}✅ The grammar is LL(1).{RESET}")
            table = createTableLL(grammar)

            print(f"{BOLD}{MAGENTA}📊 LL(1) Parsing Table:{RESET}")
            print_ll1_table(table)

            string = input(f"{BOLD}✍️  Enter a string to analyze:{RESET} ")
            StringAnalysisLL(string, table)

        elif not is_LL and is_SLR:
            # If only SLR(1)
            print(f"{CYAN}✅ The grammar is SLR(1).{RESET}")
            print_SLR_table(action, goto_table, states, new_grammar)

            string = input(f"{BOLD}✍️  Enter a string to analyze:{RESET} ")
            StringAnalysisSLR(string, action, goto_table, states, new_grammar)
            
        else:
            # If neither
            print(f"{RED}❌ The Grammar is neither LL(1) nor SLR(1).{RESET}\n")
                
    elif option == "Q":
        # Exit program
        print(f"{MAGENTA}{BOLD}👋 Bye! Thanks for using the Grammar Analyzer!{RESET}")
        exit()

    else:
        # Invalid menu option
        print(f"{RED}🚫 Invalid option. Please try again.{RESET}")
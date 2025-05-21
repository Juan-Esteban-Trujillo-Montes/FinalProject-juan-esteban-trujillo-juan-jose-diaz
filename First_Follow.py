def compute_first(grammar):
    # Create empty FIRST set for each non-terminal
    first = {}
    for nonTerminal in grammar:
        first[nonTerminal] = set()

    changed = True
    while changed:
        changed = False
        # For each non-terminal and its productions
        for nonTerminal in grammar:
            for production in grammar[nonTerminal]:
                for symbol in production:
                    # If symbol is a terminal and not in FIRST, add it
                    if not symbol.isupper() and symbol not in first:
                        first[symbol] = {symbol}
                        if symbol not in first[nonTerminal]:
                            first[nonTerminal].add(symbol)
                            changed = True
                        break
                    else:
                        # Add FIRST of symbol (except 'e') to FIRST of non-terminal
                        before = len(first[nonTerminal])
                        first[nonTerminal].update(first[symbol] - {'e'})
                        if len(first[nonTerminal]) > before:
                            changed = True
                        # If 'e' is not in FIRST of the symbol, stop
                        if 'e' not in first[symbol]:
                            break
                else:
                    # If we did not break, add 'e' to FIRST of non-terminal
                    if 'e' not in first[nonTerminal]:
                        first[nonTerminal].add('e')
                        changed = True
    return first

def compute_follow(grammar, first):
    # Create empty FOLLOW set for each non-terminal
    follow = {}
    for nonTerminal in grammar:
        follow[nonTerminal] = set()

    # Add '$' to FOLLOW of the start symbol
    start_symbol = list(grammar.keys())[0]
    follow[start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        # For each non-terminal and its productions
        for nonTerminal in grammar:
            for production in grammar[nonTerminal]:
                for i in range(len(production)):
                    symbol = production[i]
                    # Only non-terminals have FOLLOW sets
                    if symbol.isupper():
                        # If last symbol, add FOLLOW of LHS non-terminal
                        if i == len(production) - 1:
                            before = len(follow[symbol])
                            follow[symbol].update(follow[nonTerminal])
                            if len(follow[symbol]) > before:
                                changed = True
                        else:
                            next_sym = production[i + 1]
                            # If next symbol is terminal, add to FOLLOW
                            if not next_sym.isupper():
                                before = len(follow[symbol])
                                follow[symbol].add(next_sym)
                                if len(follow[symbol]) > before:
                                    changed = True
                            else:
                                # Add FIRST of next symbol (except 'e') to FOLLOW
                                before = len(follow[symbol])
                                follow[symbol].update(first[next_sym] - {'e'})
                                # If FIRST of next symbol has 'e', also add FOLLOW of LHS non-terminal
                                if 'e' in first[next_sym]:
                                    follow[symbol].update(follow[nonTerminal])
                                if len(follow[symbol]) > before:
                                    changed = True
    return follow
def compute_first(grammar):
    first = {}

    for nonTerminal in grammar:
        first[nonTerminal] = set()

    changed = True
    while changed:
        changed = False 

        for nonTerminal in grammar:
            for production in grammar[nonTerminal]:
                for symbol in production:
                    if not symbol.isupper() and symbol not in first:
                        first[symbol] = {symbol}
                        if symbol not in first[nonTerminal]:
                            first[nonTerminal].add(symbol)
                            changed = True
                        break
                    else:
                        before = len(first[nonTerminal])
                        first[nonTerminal].update(first[symbol] - {'e'})
                        if len(first[nonTerminal]) > before:
                            changed = True

                        if 'e' not in first[symbol]:
                            break
                else:
                    if 'e' not in first[nonTerminal]:
                        first[nonTerminal].add('e')
                        changed = True

    return first

def compute_follow(grammar, first):
    follow = {}

    for nonTerminal in grammar:
        follow[nonTerminal] = set()

    start_symbol = list(grammar.keys())[0]
    follow[start_symbol].add('$')

    changed = True
    while changed:
        changed = False

        for nonTerminal in grammar:
            for production in grammar[nonTerminal]:
                for i in range(len(production)):
                    symbol = production[i]

                    if symbol.isupper():
                        if i == len(production) - 1:
                            before = len(follow[symbol])
                            follow[symbol].update(follow[nonTerminal])
                            if len(follow[symbol]) > before:
                                changed = True

                        else:
                            next_sym = production[i + 1]

                            if not next_sym.isupper():
                                before = len(follow[symbol])
                                follow[symbol].add(next_sym)
                                if len(follow[symbol]) > before:
                                    changed = True

                            else:
                                before = len(follow[symbol])
                                follow[symbol].update(first[next_sym] - {'e'})

                                if 'e' in first[next_sym]:
                                    follow[symbol].update(follow[nonTerminal])

                                if len(follow[symbol]) > before:
                                    changed = True

    return follow
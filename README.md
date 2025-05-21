# FinalProject - LL(1) and SLR(1) Parsers

## Table of Contents

1. [Description](#description)
2. [Input Format](#input-format)
3. [Team Members](#team-members)
4. [System and Tools Used](#system-and-tools-used)
5. [Execution Instructions](#execution-instructions)
6. [Project Structure](#project-structure)
7. [Contact](#contact)

## Description

This project implements LL(1) and SLR(1) parsers in Python, providing tools to construct context-free grammars, build parsing tables, and analyze input strings. The project explores the fundamental concepts behind syntax analysis in compilers, focusing on two classic strategies: top-down and bottom-up parsing.

**LL(1) parsers** are a type of top-down parser that reads the input from Left to right and produces a Leftmost derivation with 1 token of lookahead. They work by predicting which production rule to use based on the current input symbol and the parser's state, making use of FIRST and FOLLOW sets. LL(1) parsers require the grammar to be free of left recursion and ambiguity, and are valued for their simplicity and efficiency in parsing many programming language constructs.

**SLR(1) parsers** (Simple LR parsers) are a form of bottom-up parser that also read Left to right and produce a Rightmost derivation in reverse. SLR(1) parsers build a finite automaton (DFA) representing possible parser states and use parsing tables constructed from LR(0) items and FOLLOW sets to decide parsing actions (shift, reduce, accept, or error). SLR(1) parsers can handle a broader class of grammars than LL(1), making them useful for more complex language structures.

By implementing both LL(1) and SLR(1) parsing techniques, this project demonstrates the algorithms behind parser table construction, grammar analysis, and the fundamental differences between predictive (LL) and shift-reduce (LR) parsing methods. The project serves as a practical introduction to compiler design theory and the internal mechanisms that support the syntax analysis phase of modern compilers.

## Input Format

The grammars used by the program are read from a plain text file (`input.txt`). Each grammar is specified as follows:

1. The first line indicates the number of production rules for the grammar (an integer).
2. The following lines are the productions, each in the format:  
   ```
   NonTerminal -> production1 production2 ...
   ```
   Each production on the right-hand side is written without spaces between its symbols. If a non-terminal has multiple productions, they are separated by spaces on the right side.
3. After all productions for one grammar, the next grammar (if any) starts with its number of productions.
4. The file may include multiple grammars, following this same pattern.

**Example:**
```
3
S -> S+T T
T -> T*F F
F -> (S) i
```

This describes a grammar with three production rules:
- `S -> S+T | T`
- `T -> T*F | F`
- `F -> (S) | i`

**Note:**  
- Use `e` to denote epsilon (the empty string).
- You can include several grammars in `input.txt`, each starting with its own number of productions.

## Team Members
- Juan Esteban Trujillo
- Juan José Díaz

Each member contributed to the system's design, development, and testing.

## System and Tools Used

To ensure compatibility and efficiency, the following tools and environments were used:

- **Operating System**: Windows 11
- **Programming Language**: Python
- **Tools**: Git

## Execution Instructions
### Steps to Run the Code

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Juan-Esteban-Trujillo-Montes/FinalProject-juan-esteban-trujillo-juan-jose-diaz.git
    cd FinalProject-juan-esteban-trujillo-juan-jose-diaz
    ```
2. Ensure you have Python installed (preferably version 3.x). You can check by running:
   ```sh
   python --version
   ```
   If Python is not installed, download and install it from [Python's official website](https://www.python.org/downloads/).
3. **Run the project** by executing the following command:
    ```sh
    python main.py
    ```

    When you run `python main.py`, the program will:
    - Automatically read all grammars defined in `input.txt`.
    - Display a menu with options such as calculating FIRST and FOLLOW sets, generating LR(0) items, building LR(0) states and transitions, and checking grammar compatibility with LL(1) or SLR(1) parsers.
    - Guide you through the process interactively, allowing you to select grammars, visualize parsing tables, and analyze input strings using either LL(1) or SLR(1) parsing techniques.

    _No additional configuration is required; just ensure `input.txt` contains your grammars in the specified format._

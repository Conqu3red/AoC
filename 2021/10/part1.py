from p1_parser import P1Parser

from parsergen.lexer import *
from parsergen.parser_utils import TokenStream

class P1Lexer(Lexer):
    LB, RB = "\\(", "\\)"
    LS, RS = "\\[", "\\]"
    LC, RC = "\\{", "\\}"
    LA, RA = "\\<", "\\>"

    ignore = ""


lookup = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

def main():
    with open("input.txt") as f:
        data = f.read().split("\n")
    
    total = 0
    for l in data:
        lexer_result = P1Lexer().lex_string(l) # get LexerResult from input
        stream = TokenStream(lexer_result) # create token stream
        parser = P1Parser(stream)
        result = parser.line()
        error = parser.error()
        if result is None and error is not None:
            end_tok = parser.fetch(parser.error_pos)
            if end_tok.type != "EOF":
                total += lookup[end_tok.value]
    
    print(f"Total: {total}")



if __name__ == "__main__":
    main()
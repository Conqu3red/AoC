# python -m parsergen chunk2.gram -o p2_parser.py

lookup = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

from parsergen.parser_utils import GeneratedParser

class P2Base(GeneratedParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.missing_chars = []
    
    def inc_score(self, end_char):
        self.missing_chars += end_char

        return True

import p2_parser

from parsergen.lexer import *
from parsergen.parser_utils import TokenStream
from part1 import P1Lexer

def main():
    with open("input.txt") as f:
        data = f.read().split("\n")
    
    scores = []
    for l in data:
        lexer_result = P1Lexer().lex_string(l) # get LexerResult from input
        stream = TokenStream(lexer_result) # create token stream
        parser = p2_parser.P2Parser(stream)
        result = parser.line()
        error = parser.error()
        if len(parser.missing_chars):
            s = 0
            for char in parser.missing_chars:
                s = 5 * s + lookup[char]
            scores.append(s)
            print("".join(parser.missing_chars), s)

    scores.sort()
    print(f"Middle Score: {scores[len(scores) // 2]}")



if __name__ == "__main__":
    main()
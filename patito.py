# Diego Martínez A01176489
# Luis Gerardo Bravo A01282014
# Proyecto DuckDuckComp

from lark import Lark
from grammar import ld_grammar
from transformer import Tables

little_duck_parser = Lark(ld_grammar, parser="lalr", start="programa", transformer=Tables())
parse = little_duck_parser.parse

fValid = open("program.txt", "r")
validSentence = fValid.read()
validTree = parse(validSentence)

print("\nPrograma:\n")
print(validTree.pretty())

from pyparsing import Word, Literal
from pyparsing import alphas, nums
from pyparsing import replaceWith, Suppress, restOfLine, ZeroOrMore, OneOrMore

equalSign = Literal("=").addParseAction(replaceWith(":"))

grammar = ZeroOrMore(equalSign)

save_file = open("mock_save.txt", "r")

tokens = grammar.parseFile(save_file)

print(tokens)

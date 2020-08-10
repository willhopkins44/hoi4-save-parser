from pyparsing import Suppress, replaceWith, Group, removeQuotes
from pyparsing import Optional, ZeroOrMore, OneOrMore, restOfLine
from pyparsing import dblQuotedString, Word, Literal, Empty, Forward
from pyparsing import alphanums, alphas8bit


def generateJSONTokens(file):
    # file = preprocess(file)

    EQ, LBRACE, RBRACE = map(Suppress, "={}")
    comment = Suppress("#") + Suppress(restOfLine)

    dblQuotedString.addParseAction(removeQuotes)
    dblQuotedString.addParseAction(
        lambda s, l, t: (t := '"' + t[0] + '"')
    )
    unquotedString = Word(alphanums + alphas8bit + "_-.:?")

    data = (dblQuotedString | unquotedString)
    prefixStrings = (dblQuotedString | unquotedString)
    obj = Forward()
    phrase = (prefixStrings + EQ + Group(obj | data))
    data_obj = OneOrMore(Group(obj)) | OneOrMore(Group(phrase)) | OneOrMore(Group(data))

    empty_obj = Empty().setParseAction(replaceWith(''))

    obj << (LBRACE + (data_obj | empty_obj) + RBRACE)

    grammar = OneOrMore(Group(phrase))
    grammar.ignore(comment)

    tokens = grammar.parseFile(file, parseAll=True)

    return tokens.asList()


def writeTokensToFile(tokens):
    output_file = open("parsed_save.txt", "w")

    for token in tokens:
        output_file.write(token)


save_file = open("analysis.hoi4", "r", encoding="utf8")
# save_file = open("mock_save.txt", "r", encoding="utf8")


print(generateJSONTokens(save_file))
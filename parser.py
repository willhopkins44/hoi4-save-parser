from pyparsing import Word, Literal
from pyparsing import alphas, nums
from pyparsing import replaceWith, Suppress, restOfLine, ZeroOrMore


def generateJSONTokens():
    stringDblQuotes = Word(alphas + nums).addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + Literal("\"") + Word(alphas + nums).addParseAction(
        lambda s, l, t: (t := ("\'" + t[0] + "\'"))
    ) + Literal("\"").addParseAction(
        replaceWith("\"")
    ) + ~Literal("=")

    stringDblQuotes = stringDblQuotes.setParseAction(lambda s, l, t: t.append(',\n'))

    # lambda explained: t[0] to access string inside token instead of t because t is the token, which includes
    # the lambda, which includes the token, which includes the lambda... max recursion error

    stringNoQuotes = Word(alphas + nums).addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + Word(alphas + nums).addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + ~Literal("=")
    stringNoQuotes = stringNoQuotes.setParseAction(lambda s, l, t: t.append(',\n'))

    dateDblQuotes = Word(alphas + nums).addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + Literal("\"").addParseAction(
        replaceWith("\"'")
    ) + Word(nums + ".") + Literal("\"").addParseAction(
        replaceWith("\'\"")
    )
    dateDblQuotes = dateDblQuotes.setParseAction(lambda s, l, t: t.append(',\n'))

    # paradoxObject = Word(alphas).addParseAction(
    #     lambda s, l, t: (t := ("\"" + t[0] + "\""))
    # ) + Literal("=").addParseAction(
    #     replaceWith(":")
    # ) + "{" + (stringDblQuotes ^ stringNoQuotes ^ dateDblQuotes) + "}"

    paradoxObject = Word(alphas).addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + "{" + restOfLine

    # comment = Suppress("#") + Suppress(restOfLine) - PROBABLY UNNECESSARY
    comment = "#" + restOfLine

    save = ZeroOrMore(stringDblQuotes) & ZeroOrMore(stringNoQuotes) & ZeroOrMore(dateDblQuotes) & ZeroOrMore(paradoxObject)

    save.ignore(comment)

    save_file = open("mock_save.txt", "r")

    tokens = save.parseFile(save_file)
    print(tokens)
    return tokens


def writeTokensToFile(tokens):
    output_file = open("parsed_save.txt", "w")

    for token in tokens:
        # output_file.write(token + "\n")
        output_file.write(token)


writeTokensToFile(generateJSONTokens())
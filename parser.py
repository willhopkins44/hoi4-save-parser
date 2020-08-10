from pyparsing import Word, Literal
from pyparsing import alphas, nums
from pyparsing import replaceWith, Suppress, restOfLine, ZeroOrMore, OneOrMore, Optional


def generateJSONTokens(file):
    stringDblQuotes = Word(alphas + nums + "_" + "-" + "(" + ")" + ".").addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + Literal("\"") + Word(alphas + nums + "_" + "-" + "(" + ")" + "." + " ").addParseAction(
        lambda s, l, t: (t := ("\'" + t[0] + "\'"))
    ) + Literal("\"").addParseAction(
        replaceWith("\"")
    ) + ~Literal("=")
    stringDblQuotes = stringDblQuotes.setParseAction(lambda s, l, t: t.append(','))

    # lambda explained: t[0] to access string inside token instead of t because t is the token, which includes
    # the lambda, which includes the token, which includes the lambda... max recursion error

    stringNoQuotes = Word(alphas + nums + "_" + "-" + "(" + ")" + ".").addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + Word(alphas + nums + "_" + "-" + "(" + ")" + ".").addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + ~Literal("=")
    stringNoQuotes = stringNoQuotes.setParseAction(lambda s, l, t: t.append(','))

    dateDblQuotes = Word(alphas + nums + "_").addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + Literal("\"").addParseAction(
        replaceWith("\"'")
    ) + Word(nums + ".") + Literal("\"").addParseAction(
        replaceWith("\'\"")
    )
    dateDblQuotes = dateDblQuotes.setParseAction(lambda s, l, t: t.append(','))

    # https://stackoverflow.com/questions/55909620/capturing-block-over-multiple-lines-using-pyparsing

    provinceLevel = Word(nums).addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + ~Literal("=")

    paradoxObject = Word(alphas + nums + "_").addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + "{" + Optional(ZeroOrMore(stringDblQuotes)) & Optional(ZeroOrMore(stringNoQuotes)) & Optional(ZeroOrMore(dateDblQuotes)) & Optional(ZeroOrMore(provinceLevel)) + "}"
    paradoxObject = paradoxObject.setParseAction(lambda s, l, t: t.append(','))

    paradoxObject = Word(alphas + nums + "_").addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + "{" + Optional(ZeroOrMore(stringDblQuotes)) & Optional(ZeroOrMore(stringNoQuotes)) & Optional(ZeroOrMore(dateDblQuotes)) & Optional(ZeroOrMore(provinceLevel)) & Optional(ZeroOrMore(paradoxObject)) + "}"
    paradoxObject = paradoxObject.setParseAction(lambda s, l, t: t.append(','))

    paradoxObject = Word(alphas + nums + "_").addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + "{" + Optional(ZeroOrMore(stringDblQuotes)) & Optional(ZeroOrMore(stringNoQuotes)) & Optional(ZeroOrMore(dateDblQuotes)) & Optional(ZeroOrMore(provinceLevel)) & Optional(ZeroOrMore(paradoxObject)) + "}"
    paradoxObject = paradoxObject.setParseAction(lambda s, l, t: t.append(','))

    paradoxObject = Word(alphas + nums + "_").addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + "{" + Optional(ZeroOrMore(stringDblQuotes)) & Optional(ZeroOrMore(stringNoQuotes)) & Optional(ZeroOrMore(dateDblQuotes)) & Optional(ZeroOrMore(provinceLevel)) & Optional(ZeroOrMore(paradoxObject)) + "}"
    paradoxObject = paradoxObject.setParseAction(lambda s, l, t: t.append(','))

    paradoxObject = Word(alphas + nums + "_").addParseAction(
        lambda s, l, t: (t := ("\"" + t[0] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + "{" + Optional(ZeroOrMore(stringDblQuotes)) & Optional(ZeroOrMore(stringNoQuotes)) & Optional(
        ZeroOrMore(dateDblQuotes)) & Optional(ZeroOrMore(provinceLevel)) & Optional(ZeroOrMore(paradoxObject)) + "}"
    paradoxObject = paradoxObject.setParseAction(lambda s, l, t: t.append(','))

    # paradoxObject = Word(alphas + nums + "_").addParseAction(
    #     lambda s, l, t: (t := ("\"" + t[0] + "\""))
    # ) + Literal("=").addParseAction(
    #     replaceWith(":")
    # ) + "{" + Optional(ZeroOrMore(stringDblQuotes)) & Optional(ZeroOrMore(stringNoQuotes)) & Optional(
    #     ZeroOrMore(dateDblQuotes)) & Optional(ZeroOrMore(provinceLevel)) & Optional(ZeroOrMore(paradoxObject)) + "}"
    # paradoxObject = paradoxObject.setParseAction(lambda s, l, t: t.append(','))

    # paradoxObject = Word(alphas + nums + "_").addParseAction(
    #     lambda s, l, t: (t := ("\"" + t[0] + "\""))
    # ) + Literal("=").addParseAction(
    #     replaceWith(":")
    # ) + "{" + Optional(ZeroOrMore(stringDblQuotes)) & Optional(ZeroOrMore(stringNoQuotes)) & Optional(
    #     ZeroOrMore(dateDblQuotes)) & Optional(ZeroOrMore(provinceLevel)) & Optional(ZeroOrMore(paradoxObject)) + "}"
    # paradoxObject = paradoxObject.setParseAction(lambda s, l, t: t.append(','))
    #
    # paradoxObject = Word(alphas + nums + "_").addParseAction(
    #     lambda s, l, t: (t := ("\"" + t[0] + "\""))
    # ) + Literal("=").addParseAction(
    #     replaceWith(":")
    # ) + "{" + Optional(ZeroOrMore(stringDblQuotes)) & Optional(ZeroOrMore(stringNoQuotes)) & Optional(
    #     ZeroOrMore(dateDblQuotes)) & Optional(ZeroOrMore(provinceLevel)) & Optional(ZeroOrMore(paradoxObject)) + "}"
    # paradoxObject = paradoxObject.setParseAction(lambda s, l, t: t.append(','))

    # Problem with the "or" (^) operator - it takes the longest match it finds and dumps the rest
    # Use "optional" operator instead

    # comment = Suppress("#") + Suppress(restOfLine) - PROBABLY UNNECESSARY
    comment = "#" + restOfLine

    save = ZeroOrMore(stringDblQuotes) & ZeroOrMore(stringNoQuotes) & ZeroOrMore(dateDblQuotes) & ZeroOrMore(paradoxObject)

    save.ignore(comment)

    tokens = save.parseFile(file)
    # tokens = save.parseFile(file, parseAll=True)
    # When finally done, use parseAll=True to raise exception if entire input is not read
    print(tokens)
    return tokens


def writeTokensToFile(tokens):
    output_file = open("parsed_save.txt", "w")

    for token in tokens:
        # output_file.write(token + "\n")
        output_file.write(token)


# save_file = open("analysis.hoi4", "r", encoding="utf8")
save_file = open("mock_save.txt", "r", encoding="utf8")

writeTokensToFile(generateJSONTokens(save_file))

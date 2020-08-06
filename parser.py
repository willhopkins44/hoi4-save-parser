from pyparsing import Word, Literal
from pyparsing import alphas, nums
from pyparsing import replaceWith, Suppress, restOfLine, ZeroOrMore


def generateJSONTokens():
    stringDblQuotes = Word(alphas).addParseAction(
        lambda s, l, t: (t := ("{\"" + s[l] + "\""))
    ) + Literal("=").addParseAction(
        replaceWith(":")
    ) + "\"" + Word(alphas) + Literal("\"").addParseAction(
        lambda s, l, t: (t := (s[l] + "}"))
    ) + ~Literal("=")

    stringDblQuotes = stringDblQuotes.setParseAction(lambda s, l, t: t.append('\n'))

    # lambda explained: s[l] instead of t is string[location] instead of token to avoid maximum recursion errors

    stringNoQuotes = Word(alphas) + Literal("=").addParseAction(replaceWith(":")) + Word(alphas) + ~Literal("=")
    stringNoQuotes = stringNoQuotes.setParseAction(lambda s, l, t: t.append('\n'))

    dateDblQuotes = Word(alphas) + Literal("=").addParseAction(replaceWith(":")) + "\"" + Word(nums) + "." + Word(nums) + "." + Word(nums) + "." + Word(nums) + "\""
    dateDblQuotes = dateDblQuotes.setParseAction(lambda s, l, t: t.append('\n'))

    # comment = Suppress("#") + Suppress(restOfLine) - PROBABLY UNNECESSARY
    comment = "#" + restOfLine

    save = ZeroOrMore(stringDblQuotes) & ZeroOrMore(stringNoQuotes) & ZeroOrMore(dateDblQuotes)

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
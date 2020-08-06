from pyparsing import Word, Literal
from pyparsing import alphas, nums
from pyparsing import replaceWith, Suppress, restOfLine, ZeroOrMore


def replace(tokens, target, replacement):
    for t in tokens:
        if t == target:
            tokens[t] = replacement

    return tokens


def generateJSONTokens():
    stringDblQuotes = Word(alphas) + "=" + "\"" + Word(alphas) + "\""
    stringDblQuotes = stringDblQuotes.setParseAction(lambda s, l, t: replace(t, "=", ":"))
    # stringDblQuotes = Literal("=").addParseAction(replaceWith(":"))
    # stringDblQuotes = stringDblQuotes.setParseAction(lambda s, l, t: t.append('\n'))

    stringNoQuotes = Word(alphas) + "=" + Word(alphas)
    # stringNoQuotes = stringNoQuotes.setParseAction(lambda s, l, t: t.append('\n'))

    dateDblQuotes = Word(alphas) + "=" + "\"" + Word(nums) + "." + Word(nums) + "." + Word(nums) + "." + Word(nums) + "\""
    # dateDblQuotes = dateDblQuotes.setParseAction(lambda s, l, t: t.append('\n'))

    # comment = Suppress("#") + Suppress(restOfLine) - PROBABLY UNNECESSARY
    comment = "#" + restOfLine

    save = ZeroOrMore(stringDblQuotes) & ZeroOrMore(stringNoQuotes) & ZeroOrMore(dateDblQuotes)

    save.ignore(comment)

    save_file = open("mock_save.txt", "r")

    save_tokens = save.parseFile(save_file)
    print(save_tokens)


def writeTokensToFile(tokens):
    output_file = open("parsed_save.txt", "w")

    for token in tokens:
        # output_file.write(token + "\n")
        output_file.write(token)


generateJSONTokens()
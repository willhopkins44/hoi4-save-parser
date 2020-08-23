import json, collections

saveTokens = []

def write_tokens_to_file(tokens):
    # outputFile = open("bundled_save.hoi4", "a", encoding="utf-8")
    # for token in tokens:
    #     outputFile.write(token)
    # outputFile.write("\n")
    # outputFile.close()
    for token in tokens:
        saveTokens.append(token)
    # saveTokens.append("\n")

from pyparsing import Suppress, replaceWith, removeQuotes
from pyparsing import sglQuotedString, Literal
def parse_JSON_to_HOI4(list_obj):
    LBRACKET, RBRACKET = map(Suppress, "[]")
    COMMA = Literal(",").setParseAction(replaceWith("="))
    sglQuotedString.setParseAction(removeQuotes)
    grammar = LBRACKET + sglQuotedString + COMMA + sglQuotedString + RBRACKET
    parseTokens = grammar.parseString(str(list_obj))
    parseTokens.append("\n")
    # print(parseTokens)
    # print([parseTokens] + ["\n"])
    write_tokens_to_file(parseTokens)


# COUNTRIES={ IS WHAT BREAKS


def recursively_parse(jsonData):
    for key in jsonData:
        if type(jsonData[key]) == dict:
            # If value is another object
            write_tokens_to_file([key, "={\n"])
            recursively_parse(jsonData[key])
            write_tokens_to_file(["}\n"])
        elif type(jsonData[key]) == list:
            for counter, item in enumerate(jsonData[key]):
                if type(item) == dict:
                    # If value is a list from duplicate keys
                    write_tokens_to_file([key, "={\n"])
                    recursively_parse(jsonData[key][counter])
                    write_tokens_to_file("}\n")
                else:
                    # Value is array of levels
                    # print(item, item[0])
                    if counter == 0:
                        write_tokens_to_file([key, "={\n"])
                    write_tokens_to_file([item])
                    if counter != (len(jsonData[key]) - 1):
                        write_tokens_to_file([" "])
                    if counter == (len(jsonData[key]) - 1):
                        write_tokens_to_file("\n}\n")
        elif len(jsonData[key]) == 0:
            # If no value
            write_tokens_to_file([key, "={\n}\n"])
        else:
            # If value is a normal value
            parse_JSON_to_HOI4([key, jsonData[key]])

# AT SOME POINT ADD HOI4TXT TO FIRST LINE

inputFile = open("parsed_save.json", "r")
open("bundled_save.hoi4", "w", encoding="utf-8").close()
jsonData = json.load(inputFile)
# json.loads is for load string input for dict output
# json.dumps is for load dictionary input for string output
# print(generate_list_tokens(format_JSON_to_tokens(jsonData)))
recursively_parse(jsonData)
# outputFile = open("bundled_save.hoi4", "a", encoding="utf-8")
# outputFile.write(saveTokens)
with open("bundled_save.hoi4", "a", encoding="utf-8") as save:
    for token in saveTokens:
        save.write(token)
# outputFile.close()
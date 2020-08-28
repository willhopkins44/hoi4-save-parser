import json, collections

saveTokens = []

def write_tokens_to_file(tokens):
    for token in tokens:
        saveTokens.append(token)

from pyparsing import Suppress, replaceWith, removeQuotes
from pyparsing import sglQuotedString, Literal
def parse_JSON_to_HOI4(list_obj):
    def removeDupe(string):
        string = string[:string.find("dupe")]
        return string
    LBRACKET, RBRACKET = map(Suppress, "[]")
    COMMA = Literal(",").setParseAction(replaceWith("="))
    sglQuotedString.setParseAction(removeQuotes)
    grammar = LBRACKET + sglQuotedString + COMMA + sglQuotedString + RBRACKET
    list_obj = [removeDupe(item) if "dupe" in item else item for item in list_obj]
    parseTokens = grammar.parseString(str(list_obj))
    parseTokens.append("\n")
    write_tokens_to_file(parseTokens)


def recursively_parse(jsonData):
    def removeDupe(string):
        if "dupe" in string:
            string = string[:string.find("dupe")]
        return string
    for key in jsonData:
        if type(jsonData[key]) == dict:
            # If value is an object
            write_tokens_to_file([removeDupe(key), "={\n"])
            recursively_parse(jsonData[key])
            write_tokens_to_file(["}\n"])
        elif type(jsonData[key]) == list:
            write_tokens_to_file([removeDupe(key), "={\n"])
            for counter, item in enumerate(jsonData[key]):
                if type(item) == dict:
                    write_tokens_to_file("{\n")
                    recursively_parse(item)
                    write_tokens_to_file("}\n")
                elif item == "":
                    # Empty object
                    write_tokens_to_file("{\n}\n")
                else:
                    # Value is array of levels or paths
                    # if counter == 0:
                    #     write_tokens_to_file("{\n")
                    write_tokens_to_file([item])
                    if counter != (len(jsonData[key]) - 1):
                        write_tokens_to_file([" "])
                    if counter == (len(jsonData[key]) - 1):
                        write_tokens_to_file("\n")
            write_tokens_to_file("}\n")
        elif len(jsonData[key]) == 0:
            # If no value
            write_tokens_to_file([removeDupe(key), "={\n}\n"])
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
    save.write("HOI4txt\n")
    for token in saveTokens:
        # print(type(token), ":", token)
        save.write(token)
# outputFile.close()
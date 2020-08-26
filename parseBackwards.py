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
    def removeDupe(string):
        string = string[:string.find("dupe")]
        return string
    LBRACKET, RBRACKET = map(Suppress, "[]")
    COMMA = Literal(",").setParseAction(replaceWith("="))
    sglQuotedString.setParseAction(removeQuotes)
    grammar = LBRACKET + sglQuotedString + COMMA + sglQuotedString + RBRACKET
    # list_obj = [item.replace("dupe", "") if "dupe" in item else item for item in list_obj]
    # for item in list_obj:
    #     if "dupe" in item:
    #         print("before:", item)
    list_obj = [removeDupe(item) if "dupe" in item else item for item in list_obj]
    # for item in list_obj:
    #     if "dupe" in item:
    #         print("after:", item)
    parseTokens = grammar.parseString(str(list_obj))
    parseTokens.append("\n")
    # for item in list_obj:
        # if item.find("dupe") != -1:
        #     print(item)
        #     # item = item[:item.find("dupe")]
        #     item = item.replace("tough", "nuts")
    # print(parseTokens)
    # print([parseTokens] + ["\n"])
    write_tokens_to_file(parseTokens)


# COUNTRIES={ IS WHAT BREAKS
# intel section
# each entry of civilian=25.000, army=10.000, etc. should NOT be prefixed with intel=
# however, this is what is happening in bundled save


def recursively_parse(jsonData):
    def removeDupe(string):
        if "dupe" in string:
            # print("before:", type(string))
            string = string[:string.find("dupe")]
            # print("after:", type(string))
        return string
    for key in jsonData:
        if type(jsonData[key]) == dict:
            # If value is another object
            # print(key)
            write_tokens_to_file([removeDupe(key), "={\n"])
            recursively_parse(jsonData[key])
            write_tokens_to_file(["}\n"])
        elif type(jsonData[key]) == list:
            # if key == "intel":
            #     write_tokens_to_file([removeDupe(key), "={\n"])
            for counter, item in enumerate(jsonData[key]):
                if type(item) == dict:
                    if key != "regional_convoys":
                        write_tokens_to_file([removeDupe(key), "={\n{\n"])
                        recursively_parse(jsonData[key][counter])
                        write_tokens_to_file("}\n}\n")
                    else:
                        write_tokens_to_file("{\n")
                        recursively_parse(jsonData[key][counter])
                        write_tokens_to_file("}\n")
                elif item == "":
                    if counter == 0:
                        write_tokens_to_file([removeDupe(key), "={\n"])
                    if counter == (len(jsonData[key]) - 1):
                        write_tokens_to_file("\n}\n")
                    write_tokens_to_file("{}\n")
                # elif key == "level":
                else:
                    # Value is array of levels or paths
                    if counter == 0:
                        write_tokens_to_file([removeDupe(key), "={\n"])
                    write_tokens_to_file([item])
                    if counter != (len(jsonData[key]) - 1):
                        write_tokens_to_file([" "])
                    if counter == (len(jsonData[key]) - 1):
                        write_tokens_to_file("\n}\n")
            # if key == "intel":
            #     write_tokens_to_file("}\n")
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
    for token in saveTokens:
        # print(type(token), ":", token)
        save.write(token)
# outputFile.close()
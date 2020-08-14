import json, collections




# FORMAT DICT (JSON) BACK INTO LIST




# def format_JSON_to_tokens(jsonData):
#     JSON_as_list = []
#     for elem in jsonData:
#         if json.dumps(jsonData[elem])[0] == "{":
#             JSON_as_list += [[elem, format_JSON_to_tokens(jsonData[elem])]]
#         elif type(jsonData[elem]) == list:
#             # reverse joining of duplicate keys
#             duplicate_key = elem
#             key_contents = jsonData[elem]
#             for counter, item in enumerate(key_contents): # enumerate provides us with the ability to use a counter
#                 JSON_as_list += [[duplicate_key, format_JSON_to_tokens(key_contents[counter])]]
#         else:
#             JSON_as_list += [[elem, [jsonData[elem]]]]
#
#     return JSON_as_list




# PARSE LIST OF TOKENS BACK INTO HOI4 GRAMMAR

# PARSE EACH LIST OBJECT INDIVIDUALLY AND PRINT INTO FILE
# NEW LINE AND REPEAT
# so generate tokens for one list at a time. Recursion should be handled outside of pyparsing





# def generate_list_tokens(listObject):
#     listTokens = []
#     for paradoxObject in listObject:
#         if len(paradoxObject) > 1:
#             listTokens += generate_list_tokens([paradoxObject[1]])
#         else:
#             if type(paradoxObject[0]) == list:
#                 print("Gotcha bitch")
#                 listTokens += generate_list_tokens(paradoxObject[0])
#             else:
#                 print("Smallest possible object:", [paradoxObject[0]], "with length", len(paradoxObject[0]), "and type", type(paradoxObject[0]))
#                 listTokens += [paradoxObject[0]]
#             # parse
#
#     return listTokens




# for each object in the dictionary, parse it
# for objects within objects, recursively parse and prepend tabs depending on level of recursion
# def parse_JSON_to_HOI4(jsonData):
#     parseTokens = []
#     for key in jsonData:
#         if type(jsonData[key]) == dict:
#             parseTokens += ([key] + [parse_JSON_to_HOI4(jsonData[key])])
#         elif type(jsonData[key]) == list:
#             parseTokens += [parse_JSON_to_HOI4(jsonData[key][0])]
#         else:
#             parseTokens += [jsonData[key]]
#     return parseTokens

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
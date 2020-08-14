from pyparsing import Suppress, replaceWith, Group, removeQuotes
from pyparsing import Optional, ZeroOrMore, OneOrMore, restOfLine
from pyparsing import dblQuotedString, Word, Literal, Empty, Forward
from pyparsing import alphanums, alphas8bit




# PARSE HOI4 SAVE DATA INTO TOKENS (PYTHON TIERED LIST)




def generate_JSON_tokens(file):
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




# FORMAT PARSED TOKENS INTO DICT (JSON)




from collections import defaultdict
import json

tree = lambda: defaultdict(tree)


def is_phrase(list_struct):
    return ((isinstance(list_struct, list)) and
            (len(list_struct) == 2) and (not isinstance(list_struct[0], list) and
            (isinstance(list_struct[1], list))))

    # A list structure is a "phrase" if it's a list, it has a head and a tail,
    # and its head is an element while its tail is a list


def convert_to_phrase(list_struct):
    return list_struct[0], list_struct[1]


def format_item(list_struct):
    if (len(list_struct) == 1) and (not isinstance(list_struct[0], list)): # If the list item is a single item
        return list_struct[0] # Return its value
    else:
        if is_phrase(list_struct[0]): # If the head is a phrase
            dic = tree()
            for elem in list_struct:
                (key, val) = convert_to_phrase(elem)
                dic = insert_check_dup(key, val, dic)
            return dic
        else:
            values = []
            for elem in list_struct:
                values.append(format_item(elem))
            return values


def insert_check_dup(key, val, dic): # insert key, val into dictionary
    if key in dic:
        if isinstance(dic[key], list):
            dic[key].append(format_item(val))
        else:
            dic[key] = [dic[key], format_item(val)]
    else:
        dic[key] = format_item(val)
    return dic


def format_tokens_to_JSON(tokens):
    dic = tree()
    for elem in tokens:
        # For each item in the list of tokens, convert it to its key value pair
        # The value might be another list. This will be handled
        (key, val) = convert_to_phrase(elem)
        dic = insert_check_dup(key, val, dic) # Insert key, value into dictionary

    return dic


def write_JSON_to_file(file, jsonData):

    file.write(json.dumps(jsonData))


save_file = open("analysis.hoi4", "r", encoding="utf8")
# save_file = open("mock_save.txt", "r", encoding="utf8")

output_file = open("parsed_save.json", "w")

tokens = generate_JSON_tokens(save_file)
jsonData = format_tokens_to_JSON(tokens)
write_JSON_to_file(output_file, jsonData)
# output_file_tokens.write(str(tokens))

# print(generate_JSON_tokens(save_file))

import json, collections




# PARSE JSON BACK INTO LIST




tree = lambda: collections.defaultdict(tree)


def format_JSON_to_tokens(jsonData):
    JSON_as_list = []
    for elem in jsonData:
        if json.dumps(jsonData[elem])[0] == "{":
            JSON_as_list += [[elem, format_JSON_to_tokens(jsonData[elem])]]
        elif type(jsonData[elem]) == list:
            duplicate_key = elem
            key_contents = jsonData[elem]
            for counter, item in enumerate(key_contents):
                JSON_as_list += [[duplicate_key, format_JSON_to_tokens(key_contents[counter])]]
            # Duplicate parent
            # First, show that you are able to backtrack to parent
        else:
            JSON_as_list += [[elem, [jsonData[elem]]]]
            # JSON_as_list += [[jsonData[elem]]]

    # reverse joining of duplicate keys

    return JSON_as_list


input_file = open("parsed_save.json", "r")
jsonData = json.load(input_file)
# json.loads is for load string input for dict output
# json.dumps is for load dictionary input for string output
print(format_JSON_to_tokens(jsonData))
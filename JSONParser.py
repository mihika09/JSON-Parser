# Before modification of the array_parser


json_whitespace = [' ', '\n', '\t', '\\n', '\\t', '\\f', '\\r']
map_whitespace = {}

""" 
have to remove the ' ' from the json_whitespace list, as when reading a string with blanks we want to read the blanks 
rather than replace it with something
"""


# Null Parser
def null_parser(s):

    if len(s) >= 4 and s[0:4] == 'null':
        return None, s[4:]

    else:
        return None


# Bool Parser
def bool_parser(s):

    if len(s) >= 4 and s[0:4] == 'true':
        return True, s[4:]

    elif len(s) >= 5 and s[0:5] == 'false':
        return False, s[5:]

    else:
        return None


# Num Parser
def num_parser(s):

    jtoken = ''
    i = 0
    l = len(s)
    while i < l and 48 <= ord(s[i]) <= 57:
        jtoken += s[i]
        i += 1

    try:
        return int(jtoken), s[i:]

    except:
        return None


# String Parser
def string_parser(s):

    s = s.strip()

    jtoken = ''

    if s[0] == '"':
        s = s[1:]
        i = 0

        while s[i] != '"':

            jtoken += s[i]
            i += 1

        if i < len(s) and s[i] == '"':
            s = s[i + 1:]
            return jtoken, s

    return None


# Array Parser
def array_parser(s):

    if s[0] == '[':
        lst = []

        # check for empty array
        if s[0:2] == '[]':
            return lst, s[2:]

        s = s[1:]
        flag = 0

        while len(s) > 0:

            while s[0] in json_whitespace:
                s = s[1:]

            tmp = value_parser(s)

            if tmp is not None:

                lst.append(tmp[0])
                s = tmp[1]

                # removing spaces before limiter (,)
                while len(s) > 0 and s[0] in json_whitespace:
                        s = s[1:]

                if s[0] == ']':
                    s = s[1:]
                    flag = 1
                    break

                elif s[0] == ',':
                    try:
                        s = s[1:]
                    except:
                        return None

                else:
                    return None

                while len(s) > 0 and s[0] in json_whitespace:
                    s = s[1:]

            else:
                return None

        if flag == 1:
            return lst, s

        else:
            return None

    else:
        return None


def object_parser(s):

    if s[0] == '{':

        flag = 0
        dct = {}

        # check for empty object
        if s[0:2] == '{}':
            return dct, s[2:]

        s = s[1:]

        while len(s) > 0:

            while s[0] in json_whitespace:
                s = s[1:]

            # print("s[0]: ", s[0], "s[1]: ", s[1])

            # checking for a
            tmp = string_parser(s)
            if tmp is not None:
                a = tmp[0]
                s = tmp[1]

            else:
                return None

            while len(s) > 0 and s[0] in json_whitespace:
                s = s[1:]

            # checking for ':' separator
            if s[0] == ':':
                s = s[1:]

            else:
                return None

            while len(s) > 0 and s[0] in json_whitespace:
                s = s[1:]

            # checking for b

            # print("s[0]b: ", s[0])
            tmp = value_parser(s)

            if tmp is not None:

                b = tmp[0]
                s = tmp[1]
                dct[a] = b

                if len(s) > 0:
                    while s[0] in json_whitespace:
                        s = s[1:]

                    if s[0] == '}':
                        s = s[1:]
                        flag = 1
                        break

                    elif s[0] == ',':
                        try:
                            s = s[1:]
                        except:
                            return None

                    else:
                        return None

                while s[0] in json_whitespace:
                    s = s[1:]

        if flag == 1:
            return dct, s

        else:
            return None

    else:
        return None


def value_parser(s):

    parsers = [null_parser, bool_parser, num_parser, string_parser, array_parser, object_parser]

    for i in parsers:

        res = i(s)
        
        if res is not None:
            return res

    return None


if __name__ == '__main__':

    file = open("/Users/mallikamohta/Desktop/JSONInput.json", "r")
    json_string = file.read()
    print(json_string)

    """while len(json_string) > 0:
        if json_string[0] in json_whitespace:
            json_string = json_string[1:]

        json_string = json_string.strip()

        print("s[0]: ", json_string[0])
        json_string = json_string[1:]"""



    r = value_parser(json_string)

    if r is None:
        print("Value Error: No JSON object could be decoded")
    else:
        print(r)

import re

check_whitespace = [' ', '\n', '\t']
map_whitespace = {"\"": "\"", "\\": '\\', "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"}


def remove_whitespace(s):

    while len(s) > 0 and s[0] in check_whitespace:
        s = s[1:]
    return s


def null_parser(s):

    s = remove_whitespace(s)
    if len(s) >= 4 and s[0:4] == 'null':
        return None, s[4:]

    return None


def bool_parser(s):

    s = remove_whitespace(s)
    if len(s) >= 4 and s[0:4] == 'true':
        return True, s[4:]

    elif len(s) >= 5 and s[0:5] == 'false':
        return False, s[5:]

    return None


def num_parser(s):

    s = remove_whitespace(s)
    x = re.search(r'^[-]?\d+(\.\d+)?([eE][+-]?\d+)?', s)
    if x:
        try:
            a = int(x.group())
        except ValueError:
            a = float(x.group())

        return a, s[x.end():]

    else:
        return None


def string_parser(s):

    s = remove_whitespace(s)

    if s[0] == '"':
        jtoken = ''
        s = s[1:]

        while s[0] != '"':

            if s[0] == '\\':
                try:
                    jtoken += map_whitespace[s[1]]
                    s = s[2:]
                except KeyError:
                    return None

            else:
                jtoken += s[0]
                s = s[1:]

        if len(s) > 0 and s[0] == '"':
            s = s[1:]
            return jtoken, s

        else:
            return None


def array_parser(s):
    s = remove_whitespace(s)

    if s[0] != '[':
        return None

    lst = []
    if s[0:2] == '[]':
        return lst, s[2:]

    s = s[1:]

    while len(s) > 0:

        tmp = value_parser(s)

        if tmp is None:
            return None

        lst.append(tmp[0])
        s = tmp[1]

        s = remove_whitespace(s)

        try:
            if s[0] == ',':
                s = s[1:]

            elif s[0] == ']':
                return lst, s[1:]

            else:
                return None

        except IndexError:
            return None

    return None


def object_parser(s):
    s = remove_whitespace(s)

    if s[0] != '{':
        return None

    dct = {}
    s = s[1:]

    try:

        while s[0] != '}':

            tmp = string_parser(s)

            if tmp is None:
                return tmp

            a, s = tmp
            s = remove_whitespace(s)

            if s[0] != ':':
                return None

            s = s[1:]
            tmp = value_parser(s)

            if tmp is None:
                return None

            dct[a], s = tmp
            s = remove_whitespace(s)
            try:
                if s[0] == ',':
                    s = s[1:]

                elif s[0] != '}':
                    return None

            except IndexError:
                return None

        return dct, s[1:]

    except IndexError:
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

    r = value_parser(json_string)

    if r is None:
        print("Value Error: No JSON object could be decoded")
    else:
        print(r)

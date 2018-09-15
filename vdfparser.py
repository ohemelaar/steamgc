import re


def parse(file):
    RE_KEY = r'^\"(?P<key>[^\"]*)\"$'
    RE_KEY_DATA = r'\g<key>'
    RE_KEY_VAL = r'^\"(?P<key>[^\"]*)\"\s*\"(?P<val>[^\"]*)\"$'
    RE_KEY_VAL_KEY = r'\g<key>'
    RE_KEY_VAL_VAL = r'\g<val>'
    RE_START_ARRAY = r'{'
    RE_END_ARRAY = r'}'

    data = {}
    while 1:
        # Reading line by line instead of using the usual for loop
        # so that we can call the parse function again on the remaining lines
        line = file.readline()
        if line == '':
            # EOF
            return data
        else:
            line = line.strip()
            if re.match(RE_KEY, line):
                # Line containing only one key
                # supposed to be followed by opening brace
                key = re.sub(RE_KEY, RE_KEY_DATA, line)
                data[key] = parse(file)
            elif re.match(RE_KEY_VAL, line):
                # Line containing one key and values
                key = re.sub(RE_KEY_VAL, RE_KEY_VAL_KEY, line)
                val = re.sub(RE_KEY_VAL, RE_KEY_VAL_VAL, line)
                data[key] = val
            elif re.match(RE_START_ARRAY, line):
                # Line containing opening brace
                pass
            elif re.match(RE_END_ARRAY, line):
                # Line containing closing brace, end of dict
                break
    return data


def serialize(data, depth=0, indent_char='\t'):
    FMT_SER_OBJ = '{2}"{0}"\n{2}{{\n{1}{2}}}\n'
    FMT_SER_STR = '{2}"{0}"\t\t"{1}"\n'

    vdf = ''
    indent = indent_char * depth
    for k, v in data.items():
        if type(v) is dict:
            vdf = vdf + FMT_SER_OBJ.format(k, serialize(v, depth + 1), indent)
        else:
            vdf = vdf + FMT_SER_STR.format(k, v, indent)

    return vdf

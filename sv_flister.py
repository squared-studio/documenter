import re
import sys
import os
from turtle import forward

INCLUDES = []
IMPORTS = []
TYPES = [
    "alias",
    "assign",
    "assert",
    "bit",
    "buf",
    "bufif0",
    "bufif1",
    "byte",
    "defparam",
    "enum",
    "event",
    "genvar",
    "int",
    "integer",
    "interface",
    "local",
    "localparam",
    "logic",
    "longint",
    "modport",
    "module",
    "nand",
    "nmos",
    "nor",
    "not",
    "notif0",
    "notif1",
    "or",
    "parameter",
    "omos",
    "pulldown",
    "pullup",
    "rand",
    "randc",
    "real",
    "realtime",
    "reg",
    "rnmos",
    "rpmos",
    "rtran",
    "rtranif0",
    "rtranif1",
    "time",
    "timeprecision",
    "timeunit",
    "tran",
    "tranif0",
    "tranif1",
    "tri",
    "tri0",
    "tri1",
    "triand",
    "trior",
    "trireg",
    "typedef",
    "virtual",
    "wire",
    "wand",
    "wor",
    "xnor",
    "xor",
]
UNKNOWN = []


def file_exists(filepath):
    return os.path.isfile(filepath)


def find_beginend(ip: str):
    opens = 0
    closes = 0
    for i in range(len(ip)):
        if ip[i] == "Á":
            opens += 1
        elif ip[i] == "À":
            closes += 1
        if opens == closes:
            break
    # print(f"BEGIN:{opens},END:{closes}")
    return ip[: i + 1]


def find_block(ip: str):
    opens = 0
    closes = 0
    for i in range(len(ip)):
        if ip[i] == "(":
            opens += 1
        elif ip[i] == ")":
            closes += 1
        if opens == closes:
            break
    # print(f"(:{opens},):{closes}")
    return ip[: i + 1]


if len(sys.argv) < 2:
    print("No input file specified")
    sys.exit()

if len(sys.argv) > 2:
    output_dir = sys.argv[2]
    if (output_dir[-1]!="/"):
        output_dir = output_dir + "/"
else:
    output_dir = "./"

with open(sys.argv[1], "r") as input_file:
    txt = input_file.read()

txt = re.sub("\t", " ", txt)
txt = re.sub("//.*", "", txt)
txt = re.sub("# *\(", "#(", txt)
txt = re.sub(r" *:: *", r"::", txt)
txt = re.sub(r" *;", ";", txt)

while "/*" in txt:
    _s = txt.find("/*")
    _e = txt.find("*/", _s)
    _t = txt[_s : _e + 2]
    txt = txt.replace(_t, "")

while "  " in txt:
    txt = txt.replace("  ", " ")

while "`include " in txt:
    _s = txt.find("`include ")
    _e = txt.find("\n", _s)
    _t = txt[_s:_e]
    txt = txt.replace(_t, "")
    _t = _t.replace("`include ", "")
    _t = _t.replace('"', "")
    INCLUDES.append(_t)
INCLUDES = list(set(INCLUDES))
INCLUDES.sort()
with open(output_dir+'includes.txt', 'a') as file:
    for item in INCLUDES:
        file.write(item + '\n')

txt = re.sub(r"\\\n", "", txt)
txt = re.sub(r"`define.*", "", txt)
txt = re.sub(r"`ifdef.*", "", txt)
txt = re.sub(r"`ifndef.*", "", txt)
txt = re.sub(r"`elsif.*", "", txt)
txt = re.sub(r"`endif.*", "", txt)

txt = txt.replace("\n", " ")
while "  " in txt:
    txt = txt.replace("  ", " ")

temp = txt.split(" ")

txt = ""
for item in temp:
    if (item == "generate") or (item == "endgenerate"):
        txt = txt + " "
    elif item == "begin":
        txt = txt + "Á "
    elif item == "end":
        txt = txt + "À "
    else:
        txt = txt + item + " "

txt = txt.replace("[", "(")
txt = txt.replace("]", ")")

txt = txt.replace("{", "(")
txt = txt.replace("}", ")")

file_type = ""
if ("module" in txt) and ("endmodule" in txt):
    file_type = "module"
elif ("interface" in txt) and ("endinterface" in txt):
    file_type = "interface"
elif ("package" in txt) and ("endpackage" in txt):
    file_type = "package"
elif ("class" in txt) and ("endclass" in txt):
    file_type = "class"
elif ("program" in txt) and ("endprogram" in txt):
    file_type = "program"
else:
    file_type = "macro"
    sys.exit()
txt = txt[: txt.find("end" + file_type)]

txt = txt[txt.find(file_type) + len(file_type) + 1 :]
file_name = re.findall("\w+", txt)
file_name = file_name[0]
txt = txt[txt.find(file_name) + len(file_name) :]
txt = re.sub("^ *", "", txt)

while txt.find("import ") == 0:
    _t = txt[: txt.find(";") + 1]
    txt = txt[txt.find(";") + 1 :]
    txt = re.sub("^ *", "", txt)
    _t = _t.replace("import ", "")
    _t = _t.replace(";", "")
    IMPORTS.append(re.sub(r"::.*", "", _t))
    TYPES.append(re.sub(r".*::", "", _t))
txt = re.sub("^ *", "", txt)

if txt[0] == "#":
    txt = txt[1:]
    params = find_block(txt)
    txt = txt.replace(params, "")
    params = params[1:-1].split(",")
    for param in params:
        param = re.sub("^ *", "", param)
        param = param[param.find(" ") + 1 :]
        first_word = param[: param.find(" ")]
        if first_word == "type":
            param = param[5:]
            TYPES.append(param[: param.find(" ")])
        if "::" in param:
            _t = re.findall(r"\w+::", param)
            _t = _t[0]
            param.replace(_t, "")
            IMPORTS.append(_t.replace("::", ""))
txt = re.sub("^ *", "", txt)

_prent = txt.find("(")
_semic = txt.find(";")
if _semic == -1:
    _semic = _prent + 10
if _prent == -1:
    _prent = _semic + 10
if _prent < _semic:
    txt = txt.replace(find_block(txt), "")

txt = re.sub("^ *; *", "", txt)

while '"' in txt:
    _s = txt.find('"')
    _e = txt.find('"', _s + 1)
    _t = txt[_s : _e + 1]
    txt = txt.replace(_t, "")

while r"::" in txt:
    _t = re.findall(r"\w+ \w+::\w+", txt)
    if len(_t) == 0:
        _t = re.findall(r"\w+::\w+", txt)
    _t = _t[0]
    if "import " in _t:
        txt = txt.replace(_t + ";", "")
        _t = _t.replace("import ", "")
    else:
        txt = txt.replace(_t, "")
    IMPORTS.append(re.sub(r"::.*", "", _t))
    TYPES.append(re.sub(r".*::", "", _t))

txt = re.sub(" *; *", ";", txt)
txt = re.sub("^ *", "", txt)

while "#" in txt:
    _s = txt.find("#")
    _t = "#" + find_block(txt[_s + 1 :])
    txt = txt.replace(_t, "")

while "always" in txt:
    _s = txt.find("always")
    _semic = txt.find(";", _s)
    _begin = txt.find("Á", _s)
    if _begin == -1:
        _begin = _semic + 10
    if _semic == -1:
        _semic = _begin + 10
    if _begin < _semic:
        _t = txt[_s : _begin + len(find_beginend(txt[_begin:]))]
        txt = txt.replace(_t, "")

while "initial" in txt:
    _s = txt.find("initial")
    _semic = txt.find(";", _s)
    _begin = txt.find("Á", _s)
    if _begin == -1:
        _begin = _semic + 10
    if _semic == -1:
        _semic = _begin + 10
    if _begin < _semic:
        _t = txt[_s : _begin + len(find_beginend(txt[_begin:]))]
        txt = txt.replace(_t, "")

while "final" in txt:
    _s = txt.find("final")
    _semic = txt.find(";", _s)
    _begin = txt.find("Á", _s)
    if _begin == -1:
        _begin = _semic + 10
    if _semic == -1:
        _semic = _begin + 10
    if _begin < _semic:
        _t = txt[_s : _begin + len(find_beginend(txt[_begin:]))]
        txt = txt.replace(_t, "")

txt = re.sub("Á *: *\w+", "Á", txt)
txt = re.sub("À *: *\w+", "À", txt)

txt = re.sub(" *\( *", " ( ", txt)
txt = re.sub(" *\) *", " ) ", txt)
txt = re.sub("` *", "`", txt)

simple_constructs = [
    "case",
    "class",
    "clocking",
    "function",
    "interface",
    "module",
    "package",
    "primitive",
    "program",
    "task",
]

for word in simple_constructs:
    while word in txt:
        # print(f">>>{word}<<<")
        txt = re.sub("  *", " ", txt)
        txt = re.sub("end" + word + " *: *\w+", "end" + word, txt)
        _s = txt.find(word)
        _e = txt.find("end" + word, _s)
        _t = txt[_s : _e + 3 + len(word)]
        _r = ""
        first_word = _t[: _t.find(" ")]
        if first_word == "case":
            _r = _t[5:-8]
            while "(" in _r:
                _tt = find_block(_r[_r.find("(") :])
                _r = _r.replace(_tt, "")
            _g = ""
            while "Á" in _r:
                _r = _r[_r.find("Á") :]
                _k = find_beginend(_r)
                _r = _r.replace(_k, "")
                _g = _g + " " + _k
            _r = _g.replace("Á", "else Á")
        txt = txt.replace(_t, _r)

txt = re.sub("^ *", "", txt)
txt = re.sub("  *", " ", txt)

txt = txt.replace("for (", "if (")
txt = txt.replace("else if (", "if (")

txt = re.sub("  *", " ", txt)

while "if (" in txt:
    _s = txt.find("if (")
    _t = "if " + find_block(txt[_s + 3 :])
    txt = txt.replace(_t, "else ")
    txt = re.sub("  *", " ", txt)

while "else " in txt:
    _s = txt.find("else ")
    if txt[_s + 5] == "Á":
        _t = "else " + find_beginend(txt[_s + 5 :])
        txt = txt.replace(_t, _t[6:-1])
    else:
        txt = txt.replace("else ", "", 1)
    txt = re.sub("  *", " ", txt)

while "(" in txt:
    _s = txt.find("(")
    _t = find_block(txt[_s:])
    txt = txt.replace(_t, "")
    txt = re.sub("  *", " ", txt)

txt = txt.split(";")

for i in range(len(txt)):
    line = re.sub("^ *", "", txt[i])
    line = re.sub(" *$", "", line)
    if ":" in line:
        line = re.sub("\w+ *: *", "", line)
    if line != "":
        first_word = line[: line.find(" ")]
        if first_word not in TYPES:
            if first_word[-2:] == "_t":
                TYPES.append(first_word)
            elif first_word[0] == "`":
                pass
            else:
                UNKNOWN.append(first_word)
        else:
            if first_word == "typedef":
                line = re.sub("^.* ", "", line)
                TYPES.append(line)
            if (first_word == "localparam") or (first_word == "parameter"):
                line = line[line.find(" ") + 1 :]
                first_word = line[: line.find(" ")]
                if first_word == "type":
                    line = line[line.find(" ") + 1 :]
                    TYPES.append(line[: line.find(" ")])

        # print(f">first_word< : >>>{line}<<<")

IMPORTS = list(set(IMPORTS))
IMPORTS.sort()
with open(output_dir+'imports.txt', 'a') as file:
    for item in IMPORTS:
        file.write(item + '\n')


TYPES = list(set(TYPES))
if "*" in TYPES:
    TYPES.remove("*")
TYPES.sort()

UNKNOWN = list(set(UNKNOWN))
if ":" in UNKNOWN:
    UNKNOWN.remove(":")
UNKNOWN.sort()
with open(output_dir+'unknown.txt', 'a') as file:
    for item in UNKNOWN:
        file.write(item + '\n')

# print(f"TYPES:{TYPES}")
# print(f"\n\n")
# print(f"FILE_TYPE:{file_type}")
# print(f"FILE_NAME:{file_name}")
# print(f"INCLUDES:{INCLUDES}")
# print(f"IMPORTS:{IMPORTS}")
# print(f"UNKNOWN:{UNKNOWN}")

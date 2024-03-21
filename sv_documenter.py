#!python

from rtl_svg import (
    draw_port_IL,
    draw_port_IOL,
    draw_port_OL,
    draw_port_IR,
    draw_port_IOR,
    draw_port_OR,
)
from rtl_svg import draw_TEXT_L, draw_TEXT_R
from general import c_header, get_block

import re
import sys
import os


def file_exists(filepath):
    return os.path.isfile(filepath)


# array of lines
lines = []

# Open the file in read mode
# remove new line char
# remove tailing spaces
with open(sys.argv[1], "r") as read_file:
    for line in read_file:
        line = re.sub("\n*", "", line)
        line = re.sub(" *$", "", line)
        line = re.sub("\t", " ", line)
        lines.append(line)

# generate header
file_author, file_description, lines = c_header(lines)

# remove lines before file type
count = 0
file_type = ""
file_name = ""
for line in lines:
    line = re.sub("^ *", "", line)
    line = re.sub("^//.*", "", line)
    line = re.sub("^`.*", "", line)
    line = re.sub(" *$", "", line)
    if line != "":
        break
    count += 1
for i in range(0, count):
    lines.pop(0)

# Convert line array to a single string & remove inline comments
str_lines = ""
for line in lines:
    line = re.sub("^ *", "", line)
    line = re.sub("//.*", "", line)
    str_lines = str_lines + line + " "
str_lines = re.sub("  *", " ", str_lines)

# get file type
file_type = str_lines[: str_lines.find(" ")]
str_lines = re.sub(f"^{file_type} *", "", str_lines)

# get file name
file_name = str_lines[: str_lines.find(" ")]
file_name = re.sub("#.*", "", file_name)
str_lines = re.sub(f"^{file_name} *", "", str_lines)

# remove initial imports
while str_lines.find("import ") == 0:
    str_lines = str_lines[str_lines.find("; ") + 2 :]

# get parameters
params = []
if str_lines[0] == "#":
    str_lines = re.sub("^# *", "", str_lines)
    file_params = get_block(str_lines)
    str_lines = str_lines.replace(file_params, "")
    params_list = file_params[1:-1].split(",")
    for param in params_list:
        if "parameter " in param:
            param_ = {}
            param = re.sub("^ *parameter *", "", param)
            param = re.sub(" *$", "", param)
            param_["def"] = re.sub("^(.*?)= *", "", param)
            param = re.sub(" *=.*", "", param)
            param_["name"] = re.sub("\[(.*?)\]", "", param)
            param_["name"] = re.sub(" *$", "", param_["name"])
            param_["name"] = re.sub(".* ", "", param_["name"])
            param_["dim"] = re.sub(".*" + param_["name"] + " *", "", param)
            param_["type"] = re.sub(" *" + param_["name"] + ".*", "", param)
            param_["des"] = ""
            for i in range(len(lines)):
                line = re.sub("//.*", "", lines[i])
                if param_["name"] in line:
                    break
            if "//" in lines[i]:
                param_["des"] = re.sub("^(.*?)// *", "", lines[i])
            else:
                while "//" in lines[i - 1]:
                    i = i - 1
                    param_["des"] = re.sub("^(.*?)// *", " ", lines[i]) + param_["des"]
            params.append(param_)


# trim initial spaces
str_lines = re.sub("^ *", "", str_lines)

# get ports
ports = []
if file_type == "module" or file_type == "program" or file_type == "interface":
    file_ports = get_block(str_lines)
    str_lines = str_lines.replace(file_ports, "")
    str_lines = re.sub("^ *", "", str_lines)
    ports_list = file_ports[1:-1].split(",")
    for port in ports_list:
        port_ = {}
        port = re.sub("^ *", "", port)
        port = re.sub(" *$", "", port)
        port_["name"] = re.sub("\[(.*?)\]", "", port)
        port_["name"] = re.sub(" *$", "", port_["name"])
        port_["name"] = re.sub("^.* ", "", port_["name"])
        port_["dim"] = port[port.find(port_["name"]) + len(port_["name"]) :]
        port_["dim"] = port_["dim"].replace(" ", "")
        port = re.sub(" *" + port_["name"] + ".*$", "", port)
        if "input " in port:
            port_["dir"] = "input"
        elif "output " in port:
            port_["dir"] = "output"
        elif "inout " in port:
            port_["dir"] = "inout"
        else:
            port_["dir"] = "interface"
        port_["type"] = re.sub("input  *|output  *|inout  *", "", port)
        port_["des"] = ""
        for i in range(len(lines)):
            line = re.sub("//.*", "", lines[i])
            if port_["name"] in line:
                break
        if "//" in lines[i]:
            port_["des"] = re.sub("^(.*?)// *", "", lines[i])
        else:
            while "//" in lines[i - 1]:
                i = i - 1
                port_["des"] = re.sub("^(.*?)// *", " ", lines[i]) + port_["des"]
        ports.append(port_)

# type closure
str_lines = re.sub("^; *", "", str_lines)
str_lines = re.sub(f" end{file_type} *", "", str_lines)

# write to file
if len(sys.argv) > 2:
    output_dir = sys.argv[2]
else:
    output_dir = "./"
if output_dir[-1] != "/":
    output_dir = output_dir + "/"


with open(output_dir + file_name + ".md", "w") as write_file:

    write_file.write(f"# {file_name} ({file_type})\n\n")

    write_file.write(f"### Author : {file_author}\n\n")

    if file_type == "module" or file_type == "program" or file_type == "interface":
        write_file.write(f"## TOP IO\n")
        write_file.write(f'<img src="./{file_name}_top.svg">\n\n')

    write_file.write(f"## Description\n{file_description}\n\n")

    if file_exists(output_dir + file_name + "_des.svg"):
        write_file.write(f'<img src="./{file_name}_des.svg">\n\n')

    write_file.write("## Parameters\n")
    write_file.write("|Name|Type|Dimension|Default Value|Description|\n")
    write_file.write("|-|-|-|-|-|\n")
    for param in params:
        write_file.write("|" + param["name"])
        write_file.write("|" + param["type"])
        write_file.write("|" + param["dim"])
        write_file.write("|" + param["def"])
        write_file.write("|" + param["des"])
        write_file.write("|\n")

    write_file.write("\n")

    if file_type == "module" or file_type == "program" or file_type == "interface":
        write_file.write("## Ports\n")
        write_file.write("|Name|Direction|Type|Dimension|Description|\n")
        write_file.write("|-|-|-|-|-|\n")
        for port in ports:
            write_file.write("|" + port["name"])
            write_file.write("|" + port["dir"])
            write_file.write("|" + port["type"])
            write_file.write("|" + port["dim"])
            write_file.write("|" + port["des"])
            write_file.write("|\n")


for __start in range(len(lines)):
    line = re.sub("//.*", "", lines[__start])
    if ports[0]["name"] in line:
        break
for __end in range(len(lines)):
    line = re.sub("//.*", "", lines[__end])
    if ports[len(ports) - 1]["name"] in line:
        break
port_lines = lines[__start : __end + 1]

__str = ""
for line in port_lines:
    __str = __str + line + "\n"
__str = re.sub("^ *//.*\n", "", __str, flags=re.MULTILINE)
port_lines = __str.split("\n")

num = 0
for port in ports:
    for i in range(len(port_lines)):
        line = re.sub(" *//.*", "", port_lines[i])
        if port["name"] in line:
            break
    ports[num]["index"] = i
    num += 1

k = -1
left_ports = []
right_ports = []
for i in range(len(ports)):
    if ports[i]["index"] != k:
        left_ports.append(-1)
        right_ports.append(-1)
        k = ports[i]["index"]
        if ports[i]["dir"] == "input":
            now_side = "l"
            left_ports.append(i)
        else:
            now_side = "r"
            right_ports.append(i)
    else:
        if now_side == "l":
            left_ports.append(i)
        else:
            right_ports.append(i)
    k = k + 1

for i in range(len(left_ports) - 1, 0, -1):
    if left_ports[i - 1] == left_ports[i]:
        left_ports.pop(i - 1)

for i in range(len(right_ports) - 1, 0, -1):
    if right_ports[i - 1] == right_ports[i]:
        right_ports.pop(i - 1)

if left_ports[0] == -1:
    left_ports.pop(0)
if right_ports[0] == -1:
    right_ports.pop(0)

if len(left_ports) > 0:
    if left_ports[len(left_ports) - 1] == -1:
        left_ports.pop(len(left_ports) - 1)
if len(right_ports) > 0:
    if right_ports[len(right_ports) - 1] == -1:
        right_ports.pop(len(right_ports) - 1)

while 1:
    if len(left_ports) < 5:
        left_ports.append(-1)
    else:
        break
    if len(left_ports) < 5:
        left_ports.insert(0, -1)
    else:
        break

while 1:
    if len(right_ports) < 5:
        right_ports.append(-1)
    else:
        break
    if len(right_ports) < 5:
        right_ports.insert(0, -1)
    else:
        break

while len(left_ports) < len(right_ports):
    left_ports.append(-1)
while len(left_ports) > len(right_ports):
    right_ports.insert(0, -1)

with open(output_dir + file_name + "_top.svg", "w") as write_file:
    write_file.write(
        f'<svg height="{140+len(left_ports)*50}" width="{140+len(left_ports)*50}" xmlns="http://www.w3.org/2000/svg">\n'
    )
    write_file.write(
        '<rect width="100%" height="100%" x="0" y="0" style="fill:white;stroke:white;stroke-width:0"/>\n'
    )
    write_file.write('<g style="fill:white;stroke:black;stroke-width:1">\n')
    write_file.write(
        f'<rect width="{len(left_ports)*50+25}" height="{len(left_ports)*50+25}" x="60" y="60"/>\n'
    )

    x = 10
    y = 85
    for i in left_ports:
        if i != -1:
            if ports[i]["dir"] == "input":
                write_file.write(draw_port_IL(x, y))
            elif ports[i]["dir"] == "output":
                write_file.write(draw_port_OL(x, y))
            else:
                write_file.write(draw_port_IOL(x, y))
            write_file.write(draw_TEXT_L(ports[i]["name"], x + 55, y))

        y = y + 50

    x = len(left_ports) * 50 + 25 + 60
    y = 85
    for i in right_ports:
        if i != -1:
            if ports[i]["dir"] == "input":
                write_file.write(draw_port_IR(x, y))
            elif ports[i]["dir"] == "output":
                write_file.write(draw_port_OR(x, y))
            else:
                write_file.write(draw_port_IOR(x, y))
            write_file.write(draw_TEXT_R(ports[i]["name"], x - 5, y))
        y = y + 50

    write_file.write("</g>\n")
    write_file.write("</svg>\n")

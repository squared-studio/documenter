#!python

from general import c_header, get_block

import re
import sys

# array of lines
lines = []

# Open the file in read mode
# remove new line char
# remove tailing spaces
with open(sys.argv[1], 'r') as read_file:
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
    line = re.sub("^ *","", line)
    line = re.sub("^//.*","", line)
    line = re.sub("^`.*","", line)
    line = re.sub(" *$","", line)
    if (line != ""):
        break
    count += 1
for i in range (0, count):
    lines.pop(0)

# Convert line array to a single string & remove inline comments
str_lines = ""
for line in lines:
    line = re.sub("^ *", "", line)
    line = re.sub("//.*", "", line)
    str_lines = str_lines + line + " "
str_lines = re.sub ("  *", " ", str_lines)

# get file type
file_type = str_lines[:str_lines.find(" ")]
str_lines = re.sub(f"^{file_type} *", "", str_lines)

# get file name
file_name = str_lines[:str_lines.find(" ")]
file_name = re.sub("#.*", "", file_name)
str_lines = re.sub(f"^{file_name} *", "", str_lines)

# remove initial imports
while (str_lines.find("import ") == 0):
    str_lines = str_lines[str_lines.find("; ")+2:]

# get parameters
file_params = ""
if (str_lines[0] == "#"):
    str_lines = re.sub("^# *", "", str_lines)
    file_params = get_block(str_lines)
    str_lines = str_lines.replace(file_params, "")

# trim initial spaces
str_lines = re.sub("^ *", "", str_lines)

# get ports
ports = []
file_ports = ""
if (file_type == "module" or file_type == "program" or file_type == "interface"):
    file_ports = get_block(str_lines)
    str_lines = str_lines.replace(file_ports, "")
    str_lines = re.sub("^ *", "", str_lines)
    ports_list = file_ports[1:-1].split(",")
    for port in ports_list:
        port_ = {}
        port = re.sub("^ *","",port)
        port = re.sub(" *$","",port)
        port_["name"] = re.sub("\[.*?\]","", port)
        port_["name"] = re.sub(" *$","", port_["name"])
        port_["name"] = re.sub("^.* ","",port_["name"])
        port_["dim"] = port[port.find(port_["name"]) + len(port_["name"]):]
        port_["dim"] = port_["dim"].replace(" ","")
        port = re.sub(" *"+port_["name"]+".*$","",port)
        if "input " in port: port_["dir"] = "input"
        elif "output " in port: port_["dir"] = "output"
        elif "inout " in port: port_["dir"] = "inout"
        else: port_["dir"] = "interface"
        port_["type"] = re.sub("input  *|output  *|inout  *", "", port)
        port_["des"] = ""
        for i in range (len(lines)):
            line = re.sub("//.*", "", lines[i])
            if (port_["name"] in line): break
        if "//" in lines[i]:
            port_["des"] = re.sub(".*?// *","",lines[i])
        else:
            while "//" in lines[i-1]:
                i = i-1
                port_["des"] = re.sub(".*?// *"," ",lines[i]) + port_["des"]
        ports.append(port_)

# type closure
str_lines = re.sub("^; *", "", str_lines)
str_lines = re.sub(f"end{file_type} *", "", str_lines)

# write to file
if (len(sys.argv) > 2):
    write_file_name = sys.argv[2]
else:
    write_file_name = "default.md"
write_file_name = "default.md"
with open(write_file_name, 'w') as write_file:
    # Header
    write_file.write(f"# {file_name} ({file_type})\n\n")
    # Author
    write_file.write(f"### Author : {file_author}\n\n")
    # Description
    write_file.write(f"{file_description}\n\n")
    # Parameters
    write_file.write("## Parameters\n")
    write_file.write("|Parameter|Type|Default Value|Description|\n")
    write_file.write("|-|-|-|-|\n")
    # Ports
    write_file.write("## Ports\n")
    write_file.write("|Port|Direction|Type|Dimension|Description|\n")
    write_file.write("|-|-|-|-|-|\n")
    for port in ports:
        write_file.write("|" + port["name"])
        write_file.write("|" + port["dir"])
        write_file.write("|" + port["type"])
        write_file.write("|" + port["dim"])
        write_file.write("|" + port["des"])
        write_file.write("|\n")


# for line in lines:
#     print(f"---{line}---")


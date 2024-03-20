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
dict_ = c_header(lines)
file_author = dict_["Author"]
file_description = dict_["Description"]
for i in range (0, dict_["Lines"]):
    lines.pop(0)

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
file_ports = ""
if (file_type == "module" or file_type == "program" or file_type == "interface"):
    file_ports = get_block(str_lines)
    str_lines = str_lines.replace(file_ports, "")
    str_lines = re.sub("^ *", "", str_lines)

# type closure
str_lines = re.sub("^; *", "", str_lines)
str_lines = re.sub(f"end{file_type} *", "", str_lines)

print(f"str_lines---{str_lines}---")
print(f"file_params---{file_params}---")
print(f"file_ports---{file_ports}---")

# write to file
if (len(sys.argv) > 2):
    write_file_name = sys.argv[2]
else:
    write_file_name = "default.md"
write_file_name = "default.md"
with open(write_file_name, 'w') as write_file:
    write_file.write(f"# {file_name} ({file_type})\n\n")
    write_file.write(f"**Author : {file_author}**\n\n")
    write_file.write(f"{file_description}\n")

# for line in lines:
#     print(f"---{line}---")


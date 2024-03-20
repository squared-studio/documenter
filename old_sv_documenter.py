#!python

import sys
import re

def get_block (ip):
    round_open_count = 0
    round_close_count = 0
    curly_open_count = 0
    curly_close_count = 0
    square_open_count = 0
    square_close_count = 0
    count = 0
    for count in range(0,len(ip)):
        if (ip[count] == "("):
            round_open_count += 1
        if (ip[count] == ")"):
            round_close_count += 1
        if (ip[count] == "("):
            curly_open_count += 1
        if (ip[count] == ")"):
            curly_close_count += 1
        if (ip[count] == "("):
            square_open_count += 1
        if (ip[count] == ")"):
            square_close_count += 1
        if (
            round_open_count == round_close_count 
            and curly_open_count == curly_close_count
            and square_open_count == square_close_count
            ):
            break
    return ip[0:count+1]
        

# read file into
with open(sys.argv[1], 'r') as file:
    svf_o = file.read()

# replace all tabs & multi-space with single space
svf_c = svf_o.replace("\t", " ")
while "  " in svf_c:
    svf_c = svf_c.replace("  ", " ")

# remove heading and tailing space
svf_c = re.sub(" *$", "", svf_c, flags=re.MULTILINE)
svf_c = re.sub("^ ", "", svf_c, flags=re.MULTILINE)

# remove all comments
svf_v = re.sub("//.*", "", svf_c)

# replace all newlines with space
svf_v = svf_v.replace("\n"," ")
svf_v = re.sub("^ *", "", svf_v)
while "  " in svf_v:
    svf_v = svf_v.replace("  ", " ")

# get file type
file_type = svf_v [:svf_v.find(" ")]
svf_v = svf_v[len(file_type)+1:]
svf_v = svf_v.replace("end"+file_type, "", 1)

# get file name
file_name = svf_v [:svf_v.find(" ")]
file_name = re.sub(" .*", "", file_name)
file_name = re.sub(";.*", "", file_name)
file_name = re.sub("#.*", "", file_name)
svf_v = svf_v[len(file_name):]
svf_v = re.sub("^ *", "", svf_v)

# get header & author
file_header = svf_o[:svf_o.find(file_type + " " + file_name)]
file_header = re.sub("^ *// ", "", file_header, flags=re.MULTILINE)
file_author = file_header[file_header.find("### Author : ")+13:file_header.find("\n", file_header.find("### Author : "))]
file_header = re.sub("### .*\n*", "", file_header, flags=re.MULTILINE)
 
# has param
if svf_v[0] == "#":
    has_param = 1
else:
    has_param = 0

params = ""
if (has_param):
    svf_v = re.sub("#", "", svf_v)
    params = get_block(svf_v)
    svf_v = svf_v.replace(params, "")
    svf_v = re.sub("^ *", "", svf_v)

ports = ""
if (file_type == "module" or file_type == "program" or file_type == "interface"):
    ports = get_block(svf_v)
    svf_v = svf_v.replace(ports, "")
    svf_v = re.sub("^ *", "", svf_v)

print(f"svf_c\n{svf_c}--------\n\n\n")
print(f"svf_v\n{svf_v}--------\n\n\n")

print(f"file_type >>> {file_type} <<< ")
print(f"file_name >>> {file_name} <<< ")
print(f"file_author >>> {file_author} <<< ")
print(f"file_header >>> {file_header} <<< ")
print(f"has_param >>> {has_param} <<< ")
print(f"params >>> {params} <<< ")
print(f"ports >>> {ports} <<< ")

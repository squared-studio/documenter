import re

# trim off tailing newline, space, tab
def trim_end (str):
    i = 0
    for i in range (len(str)-1, 0, -1):
        if (str[i] != " ") and (str[i] != "\t") and (str[i] != "\n"):
            break
    return str [0:i+1]

# returns Authoer, Description, Lines 
def c_header (line_array):
    file_description = ""
    file_author = ""
    multi_line_comment = 0 
    line_in_header = 0
    for line in line_array:
        test_line = re.sub("^ *", "", line)
        line = re.sub(" *$", "", line)
        if (test_line[0:2] == "//"):
                file_description = file_description + re.sub("^//", "", line) + "\n"
                line_in_header += 1
        elif (test_line[0:2] == "/*"):
                multi_line_comment = 1
                file_description = file_description + re.sub("^/\*", "", line) + "\n"
                line_in_header += 1
        elif (test_line[0:2] == "*/"):
                file_description = file_description + re.sub("^\*/.*", "", line) + "\n"
                multi_line_comment = 0
                line_in_header += 1
        else:
            if (multi_line_comment):
                    file_description = file_description + line + "\n"
                    line_in_header += 1
            else:
                break
    if ("Author" in file_description):
        file_author = file_description[file_description.find("Author"):file_description.find("\n", file_description.find("Author"))]
        file_author = re.sub(".*Author *: *", "", file_author)
    file_description = re.sub(".*Author.*\n*","",file_description)
    file_description = trim_end(file_description)
    return {"Author":file_author, "Description":file_description, "Lines":line_in_header}

# get block
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
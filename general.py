import re
import os


# trim off tailing newline, space, tab
def trim_end(str):
    i = 0
    for i in range(len(str) - 1, 0, -1):
        if (str[i] != " ") and (str[i] != "\t") and (str[i] != "\n"):
            break
    return str[0 : i + 1]


# returns Authoer, Description, Lines
def c_header(line_array):
    file_description = ""
    file_author = ""
    multi_line_comment = 0
    line_in_header = 0
    for line in line_array:
        test_line = re.sub(r"^ *", "", line)
        line = re.sub(r" *$", "", line)
        if test_line[0:2] == "//":
            file_description = file_description + re.sub(r"^//", "", line) + "\n"
            line_in_header += 1
        elif test_line[0:2] == "/*":
            multi_line_comment = 1
            file_description = file_description + re.sub(r"^/\*", "", line) + "\n"
            line_in_header += 1
        elif test_line[0:2] == "*/":
            file_description = file_description + re.sub(r"^\*/.*", "", line) + "\n"
            multi_line_comment = 0
            line_in_header += 1
        else:
            if multi_line_comment:
                file_description = file_description + line + "\n"
                line_in_header += 1
            else:
                break
    if "Author" in file_description:
        file_author = file_description[
            file_description.find("Author") : file_description.find(
                "\n", file_description.find("Author")
            )
        ]
        file_author = re.sub(r".*Author *: *", "", file_author)
    file_description = re.sub(r".*Author.*\n*", "", file_description)
    file_description = trim_end(file_description)
    for i in range(line_in_header):
        line_array.pop(0)
    return file_author, file_description, line_array


# get block
def get_block(ip):
    ip = ip.replace("begin", "Á")
    ip = ip.replace("end", "À")
    round_open_count = 0
    round_close_count = 0
    curly_open_count = 0
    curly_close_count = 0
    square_open_count = 0
    square_close_count = 0
    begin_count = 0
    end_count = 0
    count = 0
    for count in range(0, len(ip)):
        if ip[count] == "(":
            round_open_count += 1
        if ip[count] == ")":
            round_close_count += 1
        if ip[count] == "(":
            curly_open_count += 1
        if ip[count] == ")":
            curly_close_count += 1
        if ip[count] == "(":
            square_open_count += 1
        if ip[count] == ")":
            square_close_count += 1
        if ip[count] == "Á":
            begin_count += 1
        if ip[count] == "À":
            end_count += 1
        if (
            round_open_count == round_close_count
            and curly_open_count == curly_close_count
            and square_open_count == square_close_count
            and begin_count == end_count
        ):
            break
    ip = ip[0 : count + 1]
    ip = ip.replace("Á", "begin")
    ip = ip.replace("À", "end")
    return ip


# returns whether file exists
def file_exists(filepath):
    return os.path.isfile(filepath)


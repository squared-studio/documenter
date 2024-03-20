#!python

import sys

# Open the file in read mode ('r')
with open(sys.argv[1], 'r') as file:
    file = file.read()

print (file)


#!/usr/bin/python

from __future__ import print_function
import sys

def is_whitespace(char):
    return char in [" ", "\t"]


for filename in sys.argv[1:]:
    for i, line in enumerate(open(filename, "r")):
        if len(line)>1:
            if all(map(is_whitespace, line.rstrip())):
                print("Whitespaces in file {}, line {}".format(file, i+1))

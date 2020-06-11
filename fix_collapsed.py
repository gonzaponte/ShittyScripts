#!/usr/bin/python
import sys

assert len(sys.argv) == 2

filename      = sys.argv[1]
original_file = open(filename).read()
modified_file = original_file.replace('"metadata": {\n    "collapsed": true\n   },\n', '"metadata": {},\n')

with open(filename, "w") as file_out:
    file_out.write(modified_file)

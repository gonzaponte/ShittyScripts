#!/usr/bin/python

from __future__ import print_function
import sys

inputstr = sys.argv[1]
outputstr = "http://d24w6bsrhbeh9d.cloudfront.net/photo/{0}_700b.jpg"

ID = inputstr.split("/")[-1]
if "?" in ID:
    ID = ID[:ID.index("?")]
print(outputstr.format(ID))

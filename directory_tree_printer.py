#!/usr/bin/python

from __future__ import print_function
import os
import sys
import argparse

_inf = 1000000000

def print_folder(folder="./", prefix="", depth=_inf, skip=(), ignore_hidden=True, output_stream=sys.stdout):
    for name in sorted(os.listdir(folder)):
        if name in skip or (ignore_hidden and name[0] == "."):
            continue
        fullname = folder + name
        if os.path.isfile(fullname):
            print(prefix + name, file=output_stream)
        elif os.path.isdir(fullname):
            print(prefix + name + " --->", file=output_stream)
            if depth > 0:
                print_folder(fullname + "/", prefix + "\t", depth - 1, skip, ignore_hidden, output_stream)
            else:
                print(prefix + "\t" + "Max depth reached", file=output_stream)
        else:
            print("Not recognized:", fullname, file=output_stream)

parser = argparse.ArgumentParser(__file__)#"DirectoryTreePrinter")
parser.add_argument("-f", metavar="folder", type=str, help="root file where tree starts", required=True)
parser.add_argument("-s", metavar="folder", type=str, nargs="+", help="file or folder names to be skipped")
parser.add_argument("-l", metavar="logfile", type=str, help="log file")
parser.add_argument("-d", type=int, default=_inf, help="max depth")
parser.add_argument("--show-hidden", action="store_true", help="show hidden files")

nargs="+",
flags, extras = parser.parse_known_args(sys.argv)
if flags.s is None:
    flags.s = ()
print("Skipping the following folders:", *flags.s)
print_folder(flags.f, depth=flags.d, skip=flags.s, ignore_hidden=not flags.show_hidden, output_stream=sys.stdout if flags.l is None else open(flags.l, "w"))

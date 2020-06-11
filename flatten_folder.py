#!/usr/bin/python

import os
import sys
import shutil
import argparse

def flatten_folder(folder, to):
    for element in sorted(os.listdir(folder)):
        if element[0] == ".": continue
        fullname = os.path.join(folder, element)
        if   os.path.isdir (fullname):
            flatten_folder (fullname, to)
            shutil.rmtree(fullname)
        elif os.path.isfile(fullname) and folder != to:
            print(fullname, to)
            shutil.move(fullname, to)


parser = argparse.ArgumentParser(__file__)
parser.add_argument("folder", metavar="folder", type=str, help="folder to be flattened")
#parser.add_argument("--make-copy", action="store_true", help="do it to a separate folder")


args   = parser.parse_args()
folder = args.folder

print(folder)
flatten_folder(folder, folder)

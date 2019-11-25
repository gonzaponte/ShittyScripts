import os
import re
import sys
import glob
import argparse

def find_source_files(folder, extensions, recursive):
    source_files = []
    for name in glob.glob(os.path.join(folder, "*")):
        if os.path.isdir(name) and recursive:
            files = find_source_files(name, extensions, recursive)
            source_files.extend(files)

        if os.path.isfile(name) and any(map(name.endswith, extensions)):
            source_files.append(name)
    return source_files


def get_definitions(filename):
    definitions = []
    for line in open(filename):
        if "def " in line:
            match = re.search("(?P<fname>[a-z_]*)\(", line)
            fname = match["fname"]
            definitions.append(fname)
    return definitions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=str, help="top folder")
    parser.add_argument("-r", "--recursive", action="store_true", help="search subfolders")
    parser.add_argument("--extensions", type=str, nargs="*", default="py ipynb".split(), help="extensions to consider")

    args  = parser.parse_args(sys.argv[1:])
    files = find_source_files(args.folder, args.extensions, args.recursive)
    for file in files:
        print(file)

    for definition in get_definitions(files[1]):
        print(definition)

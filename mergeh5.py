#!/usr/env/python

import sys
import glob
import argparse

from functools import reduce

import tables as tb


def is_leaf(node):
    return not isinstance(node, tb.Group)


def is_indexed_table(node):
    return isinstance(node, tb.Table) and node.indexed


def parse_path(path):
    if not os.path.isdir(path): return (path,)

    filenames = sorted(glob.glob(os.path.join(path, "*")))
    return tuple(map(parse_path, filenames))


def flatten(items):
    flattened = []
    for item in items:
        if isinstance(item, (tuple, list)):
            flattened.extend(flatten(item))
        else:
            flattened.append(item)
    return flattened


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files_or_path", type=parse_path, nargs="*")
    parser.add_argument("-o", "--output-file", default="merged.h5")
    parser.add_argument("--overwrite", action="store_true")
    
    args = parser.parse_args(sys.argv[1:])

    first, *rest = flatten(args.input_files_or_path)

    tb.copy_file(first, args.output_file, overwrite=args.overwrite)

    to_index = {}
    with tb.open_file(args.output_file, "a") as h5out:
        for filename in rest:
            with tb.open_file(filename) as h5in:
                for node_out in filter(is_leaf, h5out.walk_nodes()):
                    path_tokens = node_out._v_pathname.split("/")[1:]
                    node_in     = reduce(getattr, path_tokens, h5in.root)

                    node_out.append(node_in[:])

                    if is_indexed_table(node_in):
                        to_index[node_out] = node_in.indexedcolpathnames

        for node, columns in to_index.items():
            print(node, columns)
            for column in columns:
                node.colinstances[column].create_index()


        h5out.flush()

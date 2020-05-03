#!/usr/env/python

import sys
import argparse

from functools import reduce

import tables as tb


def is_leaf(node):
    return not isinstance(node, tb.Group)


def is_indexed_table(node):
    return isinstance(node, tb.Table) and node.indexed



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", nargs="*")
    parser.add_argument("-o", "--output-file", default="merged.h5")
    parser.add_argument("--overwrite", action="store_true")
    
    args = parser.parse_args(sys.argv[1:])
    
    first, *rest = args.input_files

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

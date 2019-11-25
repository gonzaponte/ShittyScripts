import sys
import argparse

from itertools import combinations
from itertools import filterfalse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sum"    , type=int)
    parser.add_argument("cells"  , type=int)
    parser.add_argument("-e", "--exclude", type=int, nargs="*", default=())
    parser.add_argument("-i", "--include", type=int, nargs="*", default=())

    args  = parser.parse_args(sys.argv[1:])
    perms = combinations(range(1, 10), args.cells)
    sums  = filterfalse(lambda x: sum(x) - args.sum, perms)
    excl  = filterfalse(lambda x: any(e in x for e in args.exclude), sums)
    incl  = filter     (lambda x: all(i in x for i in args.include), excl)
    for p in incl:
        print(p)

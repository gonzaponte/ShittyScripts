#!/usr/bin/python3

import sys
import urllib
import urllib.request

def contains_tag(line):
    return "html5player.setVideoUrl" in line

def highres(line):
    return "VideoUrlHigh" in line

def lowres(line):
    return "VideoUrlLow" in line

def valid_lines(lines):
    a, b = lines
    return (lowres(a) and highres(b)) or (highres(a) and lowres(b))

def pick_link(line):
    return line.split("'")[1]

def define(line):
    if   highres(line): return "high"
    elif  lowres(line): return "low"
    else              : return "unknown"

weblink = sys.argv[1]
debug   = "--debug" in sys.argv
content = urllib.request.urlopen(weblink).read().decode()
lines   = list(filter(contains_tag, content.split("\n")))

if len(lines) > 2 or not valid_lines:
    if debug:
        for line in lines:
            print(line)
        sys.exit(1)
    raise ValueError("Invalid lines, run with --debug to check what happened")

links = {}
for line in lines:
    links[define(line)] = pick_link(line)

if debug:
    for which, link in links.items():
        print(which, link)
else:
    print(links.get("high", links.get("low", links.get("unknown"))))

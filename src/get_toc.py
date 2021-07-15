#!python
# -*- coding: utf-8 -*-

import re
import os

def get_toc(lines):
    index = 0
    count = 1
    toc = []

    while index < len(lines):
        if "<text>" in lines[index]:
            print(lines[index])
            res = re.search('<text>.+</text>', lines[index])
            if not res:
                continue
            t = res.group()[6:-7]
            index += 2
            res = re.search('".+"', lines[index])
            if not res:
                continue
            src = res.group()[1:-1]
            title = [t, src]
            toc.append(title)
            count += 1
        index += 1
    
    return title

def load(src):
    lines = None

    print(f"INFO - load file [{src}]")
    with open(src, 'r',encoding='utf-8') as f:
        lines = f.readlines()
    print(f"  Total {len(lines)} lines")
    
    return lines

def main():
    lines = load("data/src/toc.ncx")
    
    for line in lines[0: 50]:
        print(line)


    # toc = get_toc(lines)

    # for title in toc:
    #     print(title)


if __name__ == "__main__":
    main()
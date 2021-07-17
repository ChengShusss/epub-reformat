#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

def load(file):
    with open(file, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
        body = soup.findChildren(name='body')[0]

        lines = [x for x in body.children if x != '\n']

        # for line in lines[:10]:
        #     if line.findChildren(name="a"):
        #         if line.a.text == "":
        #             print(f"ERROR: {line}")
        #             line.a.decompose()
        #             print(line)
            
        return (soup, lines)

if __name__ == "__main__":
    load('data/src/index_split_000.html')

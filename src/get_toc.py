#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution

def main():
    with open("data/src/toc.ncx", 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
        ncx = soup.findChildren(name='navpoint')

        dic = []
        for item in ncx:
            text = ""
            src = ""
            for s in item.children:
                if s.name == "navlabel":
                    text = s.text.strip()
                elif s.name == "content":
                    src = s.attrs['src']
            dic.append([text, src])

        with open("data/toc.json", 'w', encoding='utf-8') as w:
            json.dump(dic, w, ensure_ascii=False)


if __name__ == "__main__":
    main()

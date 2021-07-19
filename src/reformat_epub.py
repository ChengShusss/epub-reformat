#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author: Shadow Cheng

"""

import os
import zipfile
from bs4 import BeautifulSoup


def load_document(file, label_name):
    # load html or xml file, return DOM root and all node named [label_name]
    with open(file, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
        body = soup.findChildren(name=label_name)[0]

        lines = [x for x in body.children if x != '\n']

        return (soup, lines)


def get_toc():
    # Fixed, if re-format other epub file,
    # check whether the toc file named "toc.ncx"
    #
    with open("data/src/toc.ncx", 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
        ncx = soup.findChildren(name='navpoint')

        toc = []
        for item in ncx:
            text = ""
            src = ""
            for s in item.children:
                if s.name == "navlabel":
                    text = s.text.strip()
                elif s.name == "content":
                    src = s.attrs['src']
            toc.append([text, src])

    return toc


def is_toc_prefix(toc, line):
    # whether line is title of content, return (flag-1, flag-2)
    # flag-1 indicates whether line in title
    # flag-2 indicates whether line is completed title.

    if len(line) == 0:
        return (False, False, "")
    for title in toc:
        if (line.replace(' ', '') in title.replace(' ', '')):
            if len(line) == len(title):
                return (True, True, title)
            else:
                return (True, False, title)
    return (False, False, title)


def delete_ad(lines, ad_string):
    for line in lines:
        if line.string == ad_string:
            line.decompose()


def handle_lines(lines):
    # re-format lines, merget splited lines into one line.
    index = 0
    toc = [x[0] for x in get_toc()]

    paragraph = [0, []]

    # clear cache lines
    def clear_cache():

            if paragraph[0]:
                lines[paragraph[0]].string = ""
                for tag in paragraph[1]:
                    lines[paragraph[0]].append(tag)
                paragraph[0] = 0
            paragraph[1] = []

    while (index < len(lines)):
        line = ''.join(list(lines[index].stripped_strings))

        # merge splited title
        (is_title, completed, title) = is_toc_prefix(toc, line)
        if is_title and not completed:
            t = [x for x in lines[index].find_all(name="a") if x.string]
            if t:
                t[0].string = title           
            lines[index + 1].decompose()
            index += 2
            clear_cache()
            continue

        elif is_title and completed:
            index += 1
            clear_cache()
            continue
            

        # single line contain img, omit:
        if lines[index].img:
            index += 1
            clear_cache()
            continue

        # merge splited normal lines
        if (25 < len(line)):
            
            if not paragraph[0]:
                paragraph[0] = index

            # whether single space between every char?
            if line.count(' ')/len(line) > 0.4 and "  " not in line:
                if not lines[index].string:
                    # may have tag <a> in lines[index]
                    # handle this situation
                    t = [x for x in lines[index].contents if x.string]
                    t[0].string = line.replace(' ', '')
                else:
                    lines[index].string = line.replace(' ', '')

            paragraph[1].extend(lines[index].contents)
            if not paragraph[0] and index != paragraph[0]:
                lines[index].decompose()
            
        else:
            paragraph[1].extend(lines[index].contents)
            clear_cache()
        
        # Important!
        index += 1

    # handle last paragraph
    if paragraph[0]:
        clear_cache()


def handle_document(file):
    # load file, get root and body
    (soup, lines) = load_document(file, "body")

    # define ad string
    ad_string = "更多电子书资料请搜索「书行天下」：http://www.sxpdf.com"
    delete_ad(lines, ad_string)

    # merge splited lines
    handle_lines(lines)

    for line in lines:
        if not len(line.contents):
            line.decompose()

    return soup.prettify()


def extract_epub(file, target_dir):
    # extract epub file into appointed dir
    with zipfile.ZipFile(file, 'r') as myzip:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        myzip.extractall(target_dir)
        print(f"Excart file into [{target_dir}]")


def creat_epub(target_dir, dst_name, wipe_prefix, log=False):
    # create epub file
    # walk around target dir, and push every file into epub.
    with zipfile.ZipFile(dst_name, 'w') as target:
        for i in os.walk(target_dir, topdown=False):
            for n in i[2]:
                file_path = os.path.normpath(''.join((i[0], "/", n)))
                file_path_in_zip = file_path.replace(wipe_prefix, '')
                target.write(file_path, file_path_in_zip)
                if log:
                    print(f"Write file:{file_path}->{file_path_in_zip}")


def main():
    # extract epub file into appointed dir
    extract_epub("data/src.epub", "data/src")

    # format all the .html file.
    file_list = [x for x in os.listdir("data/src") if ".html" in x]
    for file in file_list:
        print(f"Handle file: {file}")
        res = handle_document("data/src/" + file)
        with open("data/src/" + file, 'w') as f:
            f.writelines(res)

    # packaging target dir into epub file.
    creat_epub("data/src", "data/dst.epub", "data/src/", log=False)
    print("Create target File.")

def test():
    file = "data/src/index_split_000.html"
    (soup, lines) = load_document(file, "body")
    delete_ad(lines)


if __name__ == "__main__":
    main()
    # test()

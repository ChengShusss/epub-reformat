#!python
# -*- coding: utf-8 -*-

import re
import os
import zipfile

p_prefix = "<p class=\"calibre1\">"
p_suffix = "</p>"


def load_file(src):
    lines = None
    with open(src, 'r', encoding='utf-8') as f:

        print(f"[INFO] load file [{src}] ")
        lines = f.readlines()
    return lines


def get_pure_text(text) -> int:
    # exclude html label and return pure text length
    pure = re.sub('<[^>]+>', '', text)
    return pure


def handle_multi_lines(lines):
    print(f"  Total lines :{len(lines)}")
    res = []

    index = 0
    paragraph = ""
    while index < len(lines):
        cur = lines[index]

        if cur[:len(p_prefix)] == p_prefix:

            pure = cur[20:-5]
            # 去除无用的超链接
            pure = re.sub('<a id="p\d+"></a>', '', pure)
            pure_no_label = get_pure_text(pure)
            pure_len = len(pure_no_label)

            # 仅有图片超链接的行
            if pure_len == 0:
                res.append(p_prefix + paragraph + p_suffix + '\n')
                paragraph = ""
                res.append(p_prefix + pure + p_suffix + '\n')

            # 处理标题
            elif (  
                    'href' in cur and
                    (pure_no_label[0] in "一二三四五六七八九十"
                    or '章' in pure_no_label[:3]
                    or '节' in pure_no_label[:3])):
                if len(paragraph):
                    res.append(p_prefix + paragraph + p_suffix + '\n')
                    paragraph = ""
                res.append(p_prefix + pure + p_suffix + '\n')

            # 被强行分段的行
            elif 25 <= pure_len <= 45 and pure[-1] not in ['。', '！', '”', '？']:
                paragraph += pure

            # 包含多余空格的行
            elif pure_len >= 45 and pure.count(' ')/pure_len > 0.35:
                pure = ''.join(pure.split(' '))
                paragraph += pure

            # 剩余情况认为是行尾，结束该行。
            else:
                paragraph += pure
                # print(paragraph)
                res.append(p_prefix + paragraph + p_suffix + '\n')
                paragraph = ""
        else:
            if len(paragraph):
                res.append(p_prefix + paragraph + p_suffix + '\n')
                paragraph = ""
            res.append(cur)

        index += 1
    if len(paragraph) > 0:
        res.append(p_prefix + paragraph + p_suffix + '\n')

    return res


def dump(file, lines):
    with open(file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)


def get_Html_List(src):
    return [x for x in os.listdir(src) if x[-5:] == '.html']


def main():
    src = "epub-reformat/src/"
    dst = "utils/data/"
    file_list = get_Html_List(src)
    for file in file_list:

        lines = load_file(src + file)
        res = handle_multi_lines(lines)
        dump(dst + file, res)


def test():
    # with zipfile.ZipFile("data/src.epub", 'r') as myzip:
    #     if not os.path.exists("data"):
    #         os.mkdir("data")
    #     if not os.path.exists("data/src"):
    #         os.mkdir("data/src")
    #     res = myzip.extractall("data/src/")
    #     print("Excart file into data/src")

    with zipfile.ZipFile('data/dst.epub', 'w') as target:
        for i in os.walk("data/src", topdown=False):
            for n in i[2]:
                print(os.path.normpath(''.join((i[0], "/", n))))
    pass


if __name__ == "__main__":
    # main()
    test()

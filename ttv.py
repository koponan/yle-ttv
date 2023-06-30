#!/usr/bin/env python3

import argparse
import json
import math
import requests

def _digits(x: int):
    return math.floor(math.log10(x)) + 1

def _zero_pad(x: int):
    padding = "0" * (4 - _digits(x) )
    return padding + str(x)

def get_page(page: int, subpage: int):
    subpage_padded = _zero_pad(subpage)
    url = f"https://yle.fi/aihe/yle-ttv/json?P={page}_{subpage_padded}"
    res = requests.get(url)
    if not res.ok:
        return ""
    return res.text

def get_content_field(json_str):
    obj = json.loads(json_str)
    data = obj["data"]
    content = data[0]["content"]
    content_text = content["text"]
    return content_text 

def drop_html_tags(text_content):
    formatted = ""
    i = 0
    while i < len(text_content):
        c = text_content[i]
        if c == "<":
            i += 1
            while text_content[i] != ">":
                i += 1
        else:
            formatted += c
        
        i += 1

    formatted = formatted.replace("&gt;", ">")
    formatted = formatted.replace("&amp;", "&")
    return formatted

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--page", type=int, help="Page number", default=100)
    parser.add_argument("-r", "--raw", action="store_true", help="Raw HTML output")
    parser.add_argument("-m", "--subpage", type=int, help="Subpage number", default=1)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = init_args()
    json_str = get_page(args.page, args.subpage)
    if not json_str:
        print("Not found")
        exit(1)

    content = get_content_field(json_str)
    if not args.raw:
        content = drop_html_tags(content)
    
    print(content)

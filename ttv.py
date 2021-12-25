#!/usr/bin/env python3

import argparse
import json
import requests


def get_page(page: int, subpage: int):
    url = f"https://yle.fi/aihe/yle-ttv/json?P={page}_000{subpage}"
    #print(url)
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

def drop_header_and_footer(text_content):
    div_tag_attr_key = "js-yle-ttv-ttv-text\">"
    after_header = text_content.find(div_tag_attr_key) + len(div_tag_attr_key)
    h2_tag = "<h2>"
    after_h2_tag = text_content.find(h2_tag) + len(h2_tag)
    before_footer = text_content.find("</pre>")
    fmt_content = text_content[after_h2_tag:before_footer]
    return fmt_content
    
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
    #return parser
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    #parser = init_args()
    #args = parser.parse_args()
    args = init_args()
    json_str = get_page(args.page, args.subpage)
    if not json_str:
        print("Not found")
        exit(1)

    content = get_content_field(json_str)
    if not args.raw:
        #content = drop_header_and_footer(content)
        content = drop_html_tags(content)
    
    print(content)

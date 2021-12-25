import argparse
import json
import requests


def get_page(number):
    url = f"https://yle.fi/aihe/yle-ttv/json?P={number}_0001"
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
    
    return formatted

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, help="Page number", default=100)
    parser.add_argument("-r", "--raw", action="store_true", help="Raw HTML output")
    return parser


if __name__ == "__main__":
    parser = init_args()
    args = parser.parse_args()
    json_str = get_page(args.number)
    content = get_content_field(json_str)
    if not args.raw:
        #content = drop_header_and_footer(content)
        content = drop_html_tags(content)
    
    print(content)

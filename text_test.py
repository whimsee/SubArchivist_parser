import re

def replace_all(text, dic):
    if not "{\i0}" in text:
        print("check italics")
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

sub_dictionary = {
    "{\i1}" : "*",
    "{\i0}" : "*",
    }

text = "{\an7\fs14\fnArial\shad0\bord0\c&H0C0B0A&\pos(246.571,154.857)}Tell family {\i1}where{\i0} I'm going"

if any(s in text for s in ("{", "}")):
    temp_text = replace_all(text, sub_dictionary)
    sub_text = re.sub("[\{\[].*?[\}\]]", "", temp_text)
    this_line = sub_text.replace("\\N", " ").replace("\\n", " ")
    print(this_line)
import re

def replace_all(text, dic):
    if "{\i1}" in text and not "{\i0}" in text:
#         print("check italics")
        text = text.rstrip() + "{\i0}"
    if "{\i0}" in text and not "{\i1}" in text:
        text = text.strip("{\i0}")
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def clean_text(text):
    if any(s in text for s in ("{", "}")):
        temp_text = replace_all(text, sub_dictionary)
        sub_text = re.sub("[\{\[].*?[\}\]]", "", temp_text)
        this_line = sub_text.replace("\\N", " ").replace("\\n", " ")
    return this_line
    
sub_dictionary = {
    "{\i1}" : "*",
    "{\i0}" : "*",
    }

text = "{\an9}{\an7\fs14\fnArial\shad0\bord0\c&H0C0B0A&\pos(246.571,154.857)}Tell family {\i1}where{\i0} I'm {\an7\fs14\fnArial\shad0\bord0\c&H0C0B0A&\pos(246.571,154.857)}going"
text2 = "{\i1}While other countries are duking it out\\Nwith terrorism and warfare,{\i0}"
cleaned_text = clean_text(text2)
print(cleaned_text)
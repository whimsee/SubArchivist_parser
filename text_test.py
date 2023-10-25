import re

text = "{\an7\fs14\fnArial\shad0\bord0\c&H0C0B0A&\pos(246.571,154.857)}Tell family {\i1}where{\i0} I'm going"

if any(s in text for s in ("{", "}")):
    temp_text = re.sub("[\{\[].*?[\}\]]", "", text)
    this_line = text.replace("\\N", " ").replace("\\n", " ")
    print(this_line)
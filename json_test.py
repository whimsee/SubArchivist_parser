import json
import re

with open("subs/" + "Chihayafuru" + "/" + "Season_2" + "/name_dict.json") as json_data:
        name_dict = json.load(json_data)
        
print(name_dict.items())

for i, j in name_dict.items():
    if "SIGN" in i:
        print(j)
        t = j.split(",")

try:
    print(t)
    for word in t:
        if re.search(r'^' + "word" + r'$', word):
            print("true")
except NameError:
    print("no t")
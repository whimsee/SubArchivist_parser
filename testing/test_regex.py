import re
title = "How Heavy Are the Dumbbells You Lift?!:;///"

title_new = title.replace(" ","_").replace("/", "_").replace(";", "_").replace(":", "").replace(",","").replace("?","")

x = re.sub("[;:,?/;]", "", title).replace(" ", "_")

print(title_new)
print(x)
print(spaces)
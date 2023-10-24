import json
from pathlib import Path
import subprocess

with open("links.json", 'r', encoding="utf8") as file:
    data = json.load(file)
    title = data['title'].replace(" ","_")
    season = data['season'].replace(" ","_")
    
    Path("subs/" + title + "/" + season	).mkdir(parents=True, exist_ok=True)
    
    for x, y in data['episodes'].items():    
        print(x, y)
        x = x.replace(" ","_")
        subprocess.run("curl -o subs/" + title + "/" + "/" + season + "/" + x + ".ass $(crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}}' " + y + " | grep 'en-US' | awk '{print $2}')", shell=True)
#     subprocess.run("curl -o subs/DARLING_in_the_FRANXX/Season_1/E1_-_Alone_and_Lonesome.ass $(crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}}' https://www.crunchyroll.com/watch/GRDQPM1ZY/alone-and-lonesome | grep 'en-US' | awk '{print $2}')", shell=True)

# for link in links:
# 	print (subprocess.check_output("curl $(crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}}' " + link + " | grep 'en-US' | awk '{print $2}')", shell=True, text=True))



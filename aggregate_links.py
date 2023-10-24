import json
import subprocess

with open("links.json", 'r', encoding="utf8") as file:
    data = json.load(file)
    title = data['title']
    season = data['season']
    
    for x, y in data['episodes'].items():    
        print(x, y)
        subprocess.run("curl -o subs/" + title + "/" + "/" + season + "/" + x + ".ass $(crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}}' " + y + " | grep 'en-US' | awk '{print $2}')", shell=True)


# for link in links:
# 	print (subprocess.check_output("curl $(crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}}' " + link + " | grep 'en-US' | awk '{print $2}')", shell=True, text=True))



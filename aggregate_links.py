import json
from pathlib import Path
import subprocess
import shutil

with open("links.json", 'r', encoding="utf8") as file:
    data = json.load(file)
    title = data['title'].replace(" ","_").replace("'","\\'").replace("/", "//").replace(";", "_").replace(":", "")
    season = data['season'].replace(" ","_")
    
    Path("subs/" + title + "/" + season).mkdir(parents=True, exist_ok=True)
    
    for x, y in data['episodes'].items():    
        print(x, y)
        x = x.replace(" ","_").replace("'","\\'").replace(":", "-").replace("?","").replace("(", "_").replace(")","_")
        subprocess.run("curl -o subs/" + title + "/" + "/" + season + "/" + x + ".ass $(crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}}' " + y + " | grep 'en-US' | awk '{print $2}')", shell=True)
#     subprocess.run("curl -o subs/E9_-_What\\'s_done_is_done.ass $(crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}}' https://www.crunchyroll.com/watch/GD9UVJ9JN/whats-done-is-done | grep 'en-US' | awk '{print $2}')", shell=True)
    try:
        with open("subs/" + title + "/" + season + "/" + "name_dict.json", 'x') as f:
            f.write('{\n\t"All" : "All",\n\t"" : "---"\n}')
    except FileExistsError:
        pass
    
    shutil.copyfile("links.json", "subs/" + title + "/" + season + "/" + "links.json")

# for link in links:
# 	print (subprocess.check_output("curl $(crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}}' " + link + " | grep 'en-US' | awk '{print $2}')", shell=True, text=True))



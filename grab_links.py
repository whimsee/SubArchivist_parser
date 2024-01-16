import json
from pathlib import Path
import subprocess
import shutil

title = ""
season = ""
link = ""
data = {}
episodes = {}

# Read plaintext file to extract titles and subs
with open("grab.txt", 'r', encoding="utf8") as file:
    title = file.readline().rstrip('\n')
    season = file.readline().rstrip('\n')
    
    print("Title: ", title)
    print("Season :", season)
    
    folder_title = title.replace(" ","_").replace("/", "_").replace(";", "_").replace(":", "").replace(",","").replace("?","")
    link_title = title.replace(" ","_").replace("'","\\'").replace("/", "_").replace(";", "_").replace(":", "").replace("&", "\&").replace(",","").replace("?","")
    folder_season = season.replace(" ","_").replace(":", "").replace("?","")
    
    print(folder_title, link_title, folder_season)
    
    Path("subs/" + folder_title + "/" + folder_season).mkdir(parents=True, exist_ok=True)
    
    while True:
        link = file.readline().rstrip('\n')
        
        # Check end of file
        if not link:
            break
        
        episode_name = subprocess.getoutput('crunchy-cli search "' +  link + '" --audio ja-JP -o "E{{episode.number}} - {{episode.title}}"')
        
        print(episode_name, link)
        
        file_name = episode_name.replace(" ","_").replace("'","\\'").replace(":", "-").replace("?","").replace("(", "_").replace(")","_").replace("*","x").replace("&", "")
        
        subprocess.run("curl -o subs/" + folder_title + "/" + folder_season + "/" + file_name + ".ass $(crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}}' " + link + " | grep 'en-US' | awk '{print $2}')", shell=True)
        
        episodes.update({episode_name : link})
    
data = {
    "title" : title,
    "season" : season,
    "episodes" : episodes
    }

# Generate name dictionary
try:
    with open("subs/" + folder_title + "/" + folder_season + "/" + "name_dict.json", 'x') as file:
        file.write('{\n\t"All" : "All",\n\t"" : "---"\n}')
except FileExistsError:
    pass

# Generate links.json for processing
with open("subs/" + folder_title + "/" + folder_season + "/" + "links.json", "w", encoding="utf8") as file:
    json.dump(data, file,  ensure_ascii=False, indent=4)
    
    
    
import json
from pathlib import Path
import subprocess
import shutil
import re
import sys
from enum import Enum

import pycurl
from io import BytesIO

def download_image(url, save_as):
    with open("subs/" + link_title + "/" + folder_season + "/" + save_as, 'wb') as file:
        curl = pycurl.Curl()
        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, file)
        curl.perform()
        curl.close()

class AudioLocale(Enum):
    JP = "ja-JP"
    EN = "en-US"
    CN = "zh-CN"

class LkType(Enum):
    episode = "E"
    movie = "M"
    ova = "OVA"
    special = "SP"

try:
    arg = str(sys.argv[1])
    audio = AudioLocale[arg].value
except (IndexError, KeyError) as error:
    print(error, "defaulting to ja-JP")
    audio = AudioLocale["JP"].value

try:
    arg = str(sys.argv[2])
    link_type = LkType[arg].value
except (IndexError, KeyError) as error:
    print(error, "defaulting to episode")
    link_type = LkType["episode"].value

print(audio, link_type)

DEBUG = False
FAIL = False

title = ""
season = ""
link = ""
data = {}
episodes = {}

# Read plaintext file to extract titles and subs
with open("grab.txt", 'r', encoding="utf8") as file:
    title = file.readline().rstrip('\n')
    season = file.readline().rstrip('\n')
    image = file.readline().rstrip('\n')
    
    print("Title: ", title)
    print("Season: ", season)
    print("Image: ", image)
    
    folder_title = re.sub(r"['\"/;:&,?()<>.]", "", title).replace(" ", "_")
    link_title = re.sub(r"['\"/;:&,?()<>.]", "", title).replace(" ", "_")
    folder_season = re.sub(r"['\"/;:&,?()<>.]", "", season).replace(" ", "_")
    
    print(folder_title, link_title, folder_season)
    
    Path("subs/" + folder_title + "/" + folder_season).mkdir(parents=True, exist_ok=True)
    
    while True:
        body = BytesIO()
        connection = pycurl.Curl()
        
        link = file.readline().rstrip('\n')
        
        # Check end of file
        if not link:
            break
        
        episode_get = subprocess.getstatusoutput('crunchy-cli search "'
                                            + link +
                                            '" --audio '
                                            + audio +
                                            ' -o '
                                            + link_type +
                                            '"{{episode.sequence_number}} - {{episode.title}}"')
        
        episode_name = episode_get[1].replace(r"\N","")
        
        print(episode_name, link)
        
        if episode_get[0] != 0:
            print("error")
            FAIL = True
            break
        
        file_name_temp = re.sub(r"[/\"':?()*&;<>|]", "", episode_name).replace(" ", "_")
        file_name = file_name_temp[:75]
        
        if DEBUG:
        # For debugging in case crunchy-cli bugs out
            subprocess.run("curl -o subs/"
                           + link_title + "/"
                           + folder_season + "/"
                           + file_name + ".ass $(crunchy-cli search --audio "
                           + audio + " -o '{{subtitle.locale}} {{subtitle.url}}' "
                           + link + " | grep 'en-US' | awk '{print $2}')",
                           shell=True)
        
        else:
            sub_link = subprocess.getoutput("crunchy-cli search --audio '"
                                    + audio +
                                    "' -o '{{subtitle.locale}} {{subtitle.url}}' '"
                                    + link +
                                    "' | grep 'en-US' | awk '{print $2}'")
            
            if "TOO_MANY_ACTIVE_STREAMS" in sub_link:
                print("Too many active streams")
                FAIL = True
                break
            
            connection.setopt(connection.URL, sub_link)
            connection.setopt(connection.WRITEDATA, body)
            connection.perform()
            connection.close()
            sub_file = body.getvalue().decode('utf-8')
            
            with open("subs/" + link_title + "/" + folder_season + "/" + file_name + ".ass","w", encoding="utf8") as f:
                f.write(sub_file)
            
        episodes.update({episode_name : link})

if FAIL:
    print("FAILED. Check crunchy-cli or grab.txt file")
else:
    if image != "none":
        print("downloading banner")
        image_split = image.split(".")
        if image_split[len(image_split) - 1] == "png":
            download_image(image, "banner.png")
        else:
            download_image(image, "banner.jpg")
    
    data = {
        "title" : title,
        "season" : season,
        "episodes" : episodes
        }

    # Generate name dictionary
    print("Generating name_dict.json")
    try:
        with open("subs/" + folder_title + "/" + folder_season + "/" + "name_dict.json", 'x') as file:
            names = {}
            names.update({"All" : "All"})
            names.update({"NTP" : "---"})
            names.update({"" : "---"})
            json.dump(names, file,  ensure_ascii=False, indent="\t", separators=(',', ' : '))
    #         file.write('{\n\t"All" : "All",\n\t"" : "---"\n}')
    except FileExistsError:
        pass

    print("Generating links.json")
    # Generate links.json for processing
    with open("subs/" + folder_title + "/" + folder_season + "/" + "links.json", "w", encoding="utf8") as file:
        json.dump(data, file,  ensure_ascii=False, indent="\t", separators=(',', ' : '))
        
    print("DONE")
    
    
    


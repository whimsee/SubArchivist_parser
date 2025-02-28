import json
import filetype
from pathlib import Path
import subprocess
import shutil
import re
import os
import sys
from enum import Enum

import pycurl
from io import BytesIO

def download_image(url):
    with open("subs/" + link_title + "/" + folder_season + "/banner.temp", 'wb') as file:
        curl = pycurl.Curl()
        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, file)
        curl.perform()
        curl.close()
        
    kind = filetype.guess('banner.temp')
    if kind is None:
        print('Cannot guess file type!')
        return

    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)
    
    if kind.mime == "image/jpeg":
        os.rename('banner.temp', 'banner.jpg')
    elif kind.mime == "image/png":
        os.rename('banner.temp', 'banner.png')
    elif kind.mime == "image/webp":
        os.rename('banner.temp', 'banner.webp')
    else:
        print("Invalid file type")
        return
    

def get_description(file):
    temp_desc = []
    desc = ""
    NO_DESC = False

    next_line = file.readline().rstrip('\n')
    if next_line == "[[":
        print("Getting description")
        next_line = file.readline().rstrip('\n')
        while next_line != "]]":
            temp_desc.append(next_line.rstrip('\n') + "</p>")
            next_line = file.readline().rstrip('\n')
        desc = "<p>" + "<p>".join(temp_desc).rstrip('\n')
        return desc, NO_DESC
    else:
        NO_DESC = True
        return next_line, NO_DESC

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

# Initialize variables and defaults
DEBUG = False
FAIL = False
NO_DESC = False

title = ""
season = ""
link = ""
data = {}
episodes = {}
description = ""

# Read plaintext file to extract titles and subs
with open("grab.txt", 'r', encoding="utf8") as file:
    # Get info from first three lines
    title = file.readline().rstrip('\n')
    season = file.readline().rstrip('\n')
    image = file.readline().rstrip('\n')
    
    print("Title: ", title)
    print("Season: ", season)
    print("Image: ", image)
    
    folder_title = re.sub(r"['\"/;:&,?()<>.\\]", "", title).replace(" ", "_")
    link_title = re.sub(r"['\"/;:&,?()<>.\\]", "", title).replace(" ", "_")
    folder_season = re.sub(r"['\"/;:&,?()<>.\\]", "", season).replace(" ", "_")
    
    print(folder_title, link_title, folder_season)
    
    Path("subs/" + folder_title + "/" + folder_season).mkdir(parents=True, exist_ok=True)
    
    # Get description info if it exists
    description, NO_DESC = get_description(file)

    # Go through each link and process as needed
    while True:
        body = BytesIO()
        connection = pycurl.Curl()
        
        if NO_DESC and link == "":
            link = description
        else:
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
        
        file_name_temp = re.sub(r"[/\"':?()*&;<>|\\\/]", "", episode_name).replace(" ", "_")
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
        download_image(image)
    else:
        print("no banner to download")

    if NO_DESC:
        description = ""

    data = {
        "title" : title,
        "season" : season,
        "description" : description,
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
    
    print("Downloaded", len(data["episodes"]), "episodes")
    print("DONE")
    
    
    


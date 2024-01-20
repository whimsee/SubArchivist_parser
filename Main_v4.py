import json
import requests
import re

development = False
force_upload = False
name_replace = False
title_case = False

if development:
    from secrets_dev import secrets
else:
    from secrets_prod import secrets

headers = {"Authorization": "Token " + secrets['API_ID_TOKEN']}

episodes = []
source_links = []

### Easy titles from links.json ###
with open("links.json", 'r', encoding="utf8") as file:
    data = json.load(file)
    link_title = re.sub("['/;:&,?]", "", data['title']).replace(" ", "_")
    link_season = re.sub("[:?]", "", data['season']).replace(" ", "_")
    season_length = len(data['episodes'])
    for x, y in data['episodes'].items():
        episodes.append(x)
        source_links.append(y)

##### Episode info #####
index = 0
# episode_title = "E7 - Shooting Star Moratorium"         # Page
episode_title = episodes[index]
file_name = re.sub("[':?()*&]", "", episode_title).replace(" ", "_")
sub_file = "subs/" + link_title + "/" + link_season + "/" + file_name + ".ass"
# anime_title = "Laid-Back Camp"                       # Book
anime_title = data['title']
debug_title = anime_title.replace("/","_").replace("?","")
# season = "Season 2"                            # Chapter
season = data['season']
source = "Crunchyroll"
# source_link = "https://www.crunchyroll.com/watch/G63K48VZ6/shooting-star-moratorium"
source_link = source_links[index]


with open("subs/" + link_title + "/" + link_season + "/name_dict.json") as json_data:
    name_dict = json.load(json_data)

for i, j in name_dict.items():
    if "SIGN" in i:
        sign_replace = j.split(",")

# optional for lyrics
upload_lyrics = False
insert_song = False
lyrics_only = False
op_only = False
ed_only = False
OP_name = "OP - Massara"
ED_name = "ED - Stand by Me"
Insert_name = "Future Parade"

##################
# Init lists
script_info = {}
style_info = []
op_lyrics = []
ed_lyrics = []
insert_lyrics = []
dialogue = []
log = []
unhandled_lines = False


############## Functions #####################
### Multiple replace
def replace_all(text, dic):
    for i, j in pre_dictionary.items():
        text = text.replace(i, j)

    if r"{\i1}" in text and not r"{\i0}" in text:
#         print("check italics")
        if not r"{\i}" in text:
        #         print("check italics")
            text = text.rstrip() + "{\i0}"
    elif r"{\i0}" in text and not r"{\i1}" in text:
        text = text.strip(r"{\i0}")
#         text = text.replace("{\i0}","")

    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def replace_name(text, dic, tracker):
    for i, j in dic.items():
        if text == i:
            text = j
            return text
    print("Unhandled name: " + tracker + " " + text + "\n")
    log.append("Unhandled name: " + tracker + " " + text + "\n")
    return text

sub_dictionary = {
    "{\i1} " : " *",
    " {\i}" : "*",
    " {\i0}" : "* ",
    "{\i1}" : "*",
    "{\i}" : "*",
    "{\i0}" : "*"
    }

pre_dictionary = {
    "*" : "°",
    r"{\an2\i1}" : r"{\i1}",
    r"{\an8\i1}" : r"{\i1}",
    r"{\i}\N" : "{\i}<br>\n&nbsp;&nbsp;&nbsp;&nbsp;",
    r"\N": "<br>\n&nbsp;&nbsp;&nbsp;&nbsp;"
    }

def clean_text(text):
    if any(s in text for s in ("{", "}")):
#         text = text.strip("")
        temp_text = replace_all(text, sub_dictionary)
        sub_text = re.sub("[\{\[].*?[\}\]]", "", temp_text)
        this_line = sub_text.replace(r"\N", " ").replace(r"\n", " ")
#         print(this_line)
        return this_line
    else:
        return text

### Separator function for main body
def separator(next_line, type="none", format="none", extra="none"):
    
    time_in = next_line.split(",", 9)[1]
    time_hour = time_in.split(":")[0]
    time_min = time_in.split(":")[1]
    time_sec = time_in.split(":")[2].split(".")[0]
    if time_hour == "0":
        time = time_min + ":" + time_sec
    else:
        time = time_hour + ":" + time_min + ":" + time_sec
    
    # Speaker
    if not type == "SIGNS":
        if name_replace:
            temp_speaker = replace_name(next_line.split(",")[4], name_dict, next_line.split(",")[1])
        else:
            if next_line.split(",")[4] == "":
                temp_speaker = "---"
            else:
                if title_case:
                    temp_speaker = next_line.split(",")[4].title()
                else:
                    temp_speaker = next_line.split(",")[4]
            
        if extra == "flashback":
            speaker = "**" + "[" + time + "] " + "(Flashback) " + temp_speaker + "**<br>"
        elif extra == "texting":
            speaker = "**" + "[" + time + "] " + "[Texting] " + temp_speaker + "**<br>"
        elif extra == "messenger":
            speaker = "**" + "[" + time + "] " + "[Messenger] " + temp_speaker + "**<br>"
        elif extra == "song":
            speaker = "**" + "[" + time + "] " + "[SONG] " + temp_speaker + "**<br>"
        elif extra == "poem":
            speaker = "**" + "[" + time + "] " + "[POEM] " + temp_speaker + "**<br>"
        else:
            speaker = "**" + "[" + time + "] " + temp_speaker + "**<br>"
            
    # Cleaned text. Only keep inline italics.        
    base_text = clean_text(next_line.split(",", 9)[9])
#     print(base_text)
    
    ## Default setting
    if type == "DEFAULT":
        ## FORMAT: &nbsp;&nbsp;&nbsp;&nbsp;this is a line<br>
        ## For multiline
        if len(base_text.rstrip().split(r"\N")) >= 2:
            separate_lines = []
            for text in base_text.split(r"\N"):
                temp_line = text.rstrip()
                if format == "italics":
                    separate_lines.append("*&nbsp;&nbsp;&nbsp;&nbsp;" + temp_line.lstrip() + "*<br>")
                else:
                    separate_lines.append("&nbsp;&nbsp;&nbsp;&nbsp;" + temp_line + "<br>")
            joined_line = "".join(separate_lines)
            this_line = joined_line.replace(r"\h", " ")
            if "{" in this_line:
                log.append("Unhandled line: " + this_line + "\n")
            dialogue.append(speaker + this_line)
        else:
        ## For single line
            temp_line = base_text.rstrip().split(r"\N")[0]
            if format == "italics":
                formatted_line = "&nbsp;&nbsp;&nbsp;&nbsp;*" + temp_line + "*<br>"
            else:
                formatted_line = "&nbsp;&nbsp;&nbsp;&nbsp;" + temp_line + "<br>"
            this_line = formatted_line.replace(r"\h", " ")
            if "{" in this_line:
                log.append("Unhandled line: " + this_line + "\n")
            dialogue.append(speaker + this_line)
    
    ## For song lyrics (present as is with <br> between lines)
    elif type == "LYRICS":
        if len(base_text.rstrip().split(r"\N")) >= 2:
            separate_lines = []
            for text in base_text.split(r"\N"):
                temp_line = text.rstrip()
                separate_lines.append(temp_line + "<br>")
            this_line = "".join(separate_lines)
        else:
            this_line = base_text.rstrip().split(r"\N")[0]
        if extra == "OP":
            op_lyrics.append(this_line)
        if extra == "ED":
            ed_lyrics.append(this_line)
        if extra == "EXTRA":
            insert_lyrics.append(this_line)
    
    elif type == "SIGNS":
        this_line = base_text.replace(r"\N", " ").replace(r"\n", " ").replace(r"\h", " ")
        dialogue.append("***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;" + this_line + "<br>")
    
    # If unhandled
    else:
        print("Unhandled line: " + time_in + " " + mode + " " + next_line.split(",", 9)[4] + " " + base_text)
        log.append("Unhandled line: " + time_in + " " + mode + " " + next_line.split(",", 9)[4] + " " + base_text)

### API GET
def API_get(target, type="list", ID=0):
    
    if type == "list":
        if target == "book":
            response = requests.get(secrets['book_url'], headers=headers)
        elif target == "chapter":
            response = requests.get(secrets['chapter_url'], headers=headers)
        elif target == "page":
            response = requests.get(secrets['page_url'], headers=headers)
        
        return(response.json())
    
    if type == "read":
        if target == "book":
            response = requests.get(secrets['book_url'] + str(ID), headers=headers)
        elif target == "chapter":
            response = requests.get(secrets['chapter_url'] + str(ID), headers=headers)
        elif target == "page":
            response = requests.get(secrets['page_url'] + str(ID), headers=headers)
        
        return(response.json())
        
### Main Loop ###############################################################################################
print("(" + str(index + 1) + "/" + str(season_length) + ") " + episode_title) 

with open(sub_file, "r", encoding="utf8") as file:
    ## Header for source, metadata, etc.
    dialogue.append("Source: [" + source + "](" + source_link + ")<br>")
    dialogue.append("\n")
    op_lyrics.append("Source: [" + source + "](" + source_link + ")<br>")
    ed_lyrics.append("Source: [" + source + "](" + source_link + ")<br>")
    insert_lyrics.append("Source: [" + source + "](" + source_link + ")<br>")
    
    dialogue.append("Translator:<br>")
    dialogue.append("\n")
    op_lyrics.append("Translator:<br>")
    ed_lyrics.append("Translator:<br>")
    insert_lyrics.append("Translator:<br>")
    
    dialogue.append("Editor:<br>")
    dialogue.append("\n")
    op_lyrics.append("Editor:<br>")
    op_lyrics.append("\n")
    ed_lyrics.append("Editor:<br>")
    ed_lyrics.append("\n")
    insert_lyrics.append("Editor:<br>")
    insert_lyrics.append("\n")
    
    dialogue.append("Timer:<br>")
    dialogue.append("\n")
    
    dialogue.append("QC:<br>")
    dialogue.append("\n")
    
    dialogue.append("(Please feel free to edit the speaker names if incomplete or inaccurate. Names are handled on a best-effort basis depending on the info on the source file. Dialogue is left as is.)<br>")
    dialogue.append("\n")
    
    ## Loop for metadata-type data (Script Info)
    file.readline()
    while True:
        next_line = file.readline()
        
        if not next_line:
            break
        elif next_line == "[V4+ Styles]\n":
            break
        
        if "Original Script" in next_line:
            this_line = next_line.split(": ")[1].split("  [")[0]
            script_info.update({"Original_Script" : this_line + "\n"})
        elif next_line == "\n":
            pass
        else:
            this_line = next_line.split(": ")
            try:
                script_info.update({this_line[0] : this_line[1]})
            except IndexError:
                script_info.update({this_line[0] : "\n"})
    
    ## Start another loop for Styles
    while True:
        next_line = file.readline()
        
        if not next_line:
            break
        elif next_line == "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n":
            break
        if next_line == "[Events]\n" or next_line == "\n" or next_line == "Format:\n" or next_line == "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,Strikeout,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n":
            pass
        else:
            style_info.append(next_line.split(",")[0].split(": ")[1])
        
    ## Start another loop for dialogue events (Events). Uses separator
    while True:
        sign_found = False
        next_line = file.readline()
        if not next_line:
            break
        
        mode = next_line.split(",")[3].lower()
        agent = next_line.split(",")[4].lower()
#         print(next_line, mode)
        if mode == "songs_op":
            separator(next_line, type="LYRICS", extra="OP")      
        elif mode == "songs_ed":
            separator(next_line, type="LYRICS", extra="ED")
        elif mode == "songs_insert":
            separator(next_line, type="LYRICS", extra="EXTRA")
        elif any(s in mode for s in ("default", "main", "top", "bd dx",
                                     "dx", "top dx", "narration", "any",
                                     "whitesmall", "bluesmall", "bluetext", "whitetext",
                                     "narrator", "question", "4-koma", "s01", "chiha-overlap",
                                     "left", "right"
                                     )):
            if any(s in agent for s in (
                "sign", "board", "desk", "note", "book", "text", "paper",
                "tape", "title", "nameplate", "notice", "sheet", "calendar",
                "phone screen", "building", "exhibition", "phone", "leaflet",
                "wall", "screen", "slate", "next", "alt", "preview", "eyecatch",
                "caption", "card", "form"
                )):
                separator(next_line, type="SIGNS")
            elif "italic" in mode:
                separator(next_line, type="DEFAULT", format="italics")
            else:
                separator(next_line, type="DEFAULT")
        elif any(s in mode for s in ("italic", "internal", "innerthought", "thought")):
            separator(next_line, type="DEFAULT", format="italics")
        elif "texting" in mode:
            separator(next_line, type="DEFAULT", extra="texting")
        elif any(s in mode for s in ("song", "song_lyrics", "lyricsromajibd"
                                     )):
            separator(next_line, type="DEFAULT", extra="song")
        elif any(s in mode for s in ("messenger", "phone", "tweet", "cell", "messages2",
                                     "messages", "bbs1", "bbs2"
                                     )):
            separator(next_line, type="DEFAULT", extra="messenger")	
        elif "flashback" in mode:
            separator(next_line, type="DEFAULT", extra="flashback")
        elif "chiha-poem" in mode:
            separator(next_line, type="DEFAULT", extra="poem")
        elif any(s in mode for s in (
            "sign", "sfx", "eyecatch", "next_chapter", "illustration", "next ep",
            "os", "ep title", "epnum", "generic caption", "preview", "fromhere",
            "sine", "title", "setting", "disclaimer",
            "next time", "card", "building", "door", "nextep", "tvlogo",
            "note", "paper", "script", "green room", "movie",
            "advert", "cd", "banner", "golden", "text", "tracks", "goal", "radio show",
            "whiteboard", "tv anime", "next_time", "midlow", "next-time", "game"
            )):
            separator(next_line, type="SIGNS")
        
        # Catches unhandled lines
        else:
            try:
                for word in sign_replace:
                    if re.search(r'^' + mode + r'$', word):
                        sign_found = True
            except NameError:
                pass
            
            if sign_found:
                separator(next_line, type="SIGNS")
            elif any(s in agent for s in (
                "fx", "text", "sign", "shirt", "eyecatch", "label", "title", "banner",
                "stamp", "card", "door", "tv", "envelope", "box", "caption"
                )):
                separator(next_line, type="SIGNS")
            elif any(s in agent for s in (
                "phone", "site"
                )):
                separator(next_line, type="DEFAULT", extra="messenger")
            else:
                separator(next_line)

## Check for unhandled lines and aborts upload
for text in log: 
    if "Unhandled line:" in text:
        unhandled_lines = True
        if (force_upload == True):
            print("Upload aborted but forced anyway. Check log for unhandled lines.")
        else:
            print("Upload aborted. Check log for unhandled lines.")
        break
    
    if "Unhandled name:" in text:
        unhandled_lines = True
        if (force_upload == True):
            print("Upload aborted but forced anyway. Check log for unhandled name.")
        else:
            print("Upload aborted. Check log for unhandled name.")
        break

#### For debug
# unhandled_lines = True
# full_dialogue = "\n".join(dialogue)
# for text in dialogue:
#     print(text)

# print(this_line)
# print(op_lyrics)
# print(ed_lyrics)

# print(op_lyrics_full)
# print("---------")
# print(ed_lyrics_full)
# text_extract.update({"ed_lyrics" : ed_lyrics_full})
# print(script_info)

### Joining arrays for dumps ###########################
## Dialogue
full_dialogue = "".join(dialogue)
with open('dumps/' + debug_title + '-' + file_name + '-dialogue-dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(full_dialogue))

## Lyrics
if upload_lyrics or lyrics_only:
    
    if not ed_only:
        op_lyrics_full = "<br>".join(op_lyrics)
        with open('dumps/' + debug_title + '-' + OP_name + '-lyrics-dump.txt', 'w', encoding="utf8") as f:
            f.write(json.dumps(op_lyrics_full))
    
    if not op_only:
        ed_lyrics_full = "<br>".join(ed_lyrics)
        with open('dumps/' + debug_title + '-' + ED_name + '-lyrics-dump.txt', 'w', encoding="utf8") as f:
            f.write(json.dumps(ed_lyrics_full))
        
if insert_song:
    insert_lyrics_full = "<br>".join(insert_lyrics)
    with open('dumps/' + debug_title + '-' + Insert_name + '-lyrics-dump.txt', 'w', encoding="utf8") as f:
        f.write(json.dumps(insert_lyrics_full))

####################################
## FULL API SEQUENCE
if not unhandled_lines or force_upload:
    print("Uploading", episode_title)
## Book search and create
#     Init vars
    todo = ""
    BOOK_ID = 0
    found = False
    

    response = requests.get(secrets['book_url']+"?count=300&sort=-created_at", headers=headers)
    list = response.json()

    for data in list['data']:
        if anime_title in data['name']:
            BOOK_ID = data['id']
            found = True
            log.append("Anime: " + data['name'] + "\n")
            break
        
    if not found:
        # add to log
        log.append("Anime not found. Creating " + anime_title + "\n")
        todo = {
            "name": anime_title,
            "description": "If that book isn't here"
        }
        response = requests.post(secrets['book_url'], json=todo, headers=headers)
        BOOK_ID = response.json()['id']
        

    ## Chapter search and create
    todo = ""
    CHAPTER_ID = 0
    count = 0
    offset = 0
    found = False

    response = requests.get(secrets['chapter_url']+"?count=300&sort=-created_at", headers=headers)
    list = response.json()
    for data in list['data']:
        if str(BOOK_ID) in str(data['book_id']):
            if data['name'] == season:
                # add to log
                log.append("Season found\n")
                CHAPTER_ID = data['id']
                found = True
                break

    if not found:
        # add to log
        log.append("Season not found. Adding " + season + "\n")
        todo = {
            "book_id": BOOK_ID,
            "name": season
        }
        response = requests.post(secrets['chapter_url'], json=todo, headers=headers)
        CHAPTER_ID = response.json()['id']

    ## POST PAGE
    todo = ""
    found = False

    if not lyrics_only:
        todo = {
            "book_id": BOOK_ID,
            "chapter_id": CHAPTER_ID,
            "name": episode_title,
            "markdown": full_dialogue,
        }

        response = requests.post(secrets['page_url'], json=todo, headers=headers)
        # log this
        log.append(str(response.status_code) + " " + episode_title + " added\n")

    if upload_lyrics or lyrics_only:
        
        if not ed_only:
        # OP
            print("uploading song", OP_name)
            todo = {
                "book_id": BOOK_ID,
                "chapter_id": CHAPTER_ID,
                "name": OP_name,
                "markdown": op_lyrics_full
                }
            response = requests.post(secrets['page_url'], json=todo, headers=headers)
            log.append(str(response.status_code) + " " + OP_name + " added\n")
        
        if not op_only:
        # ED
            print("uploading song", ED_name)
            todo = {
                "book_id": BOOK_ID,
                "chapter_id": CHAPTER_ID,
                "name": ED_name,
                "markdown": ed_lyrics_full
                }
            response = requests.post(secrets['page_url'], json=todo, headers=headers)
            log.append(str(response.status_code) + " " + ED_name + " added\n")
        
    if insert_song:
        print("uploading song", Insert_name)
        # Insert song
        todo = {
            "book_id": BOOK_ID,
            "chapter_id": CHAPTER_ID,
            "name": Insert_name,
            "markdown": insert_lyrics_full
            }
        response = requests.post(secrets['page_url'], json=todo, headers=headers)
        log.append(str(response.status_code) + " " + ED_name + " added\n")
        

## Handle log
lines = len(dialogue)
for x, y in script_info.items():
    log_text = x + ": " + y
    log.append(log_text)

log.append("\n")
log.append("\n".join(style_info))
log.append("\n")
log.append("\n")
log.append(str(lines) + " lines")
log_full = "".join(log)
    
with open('dumps/' + debug_title + '-' + file_name + '-log.txt', 'w', encoding="utf8") as f:
    f.write(log_full)
# 
print("DONE " + str(lines) + " lines")
import json
from secrets import secrets
import requests

headers = {"Authorization": "Token " + secrets['API_ID_TOKEN']}

##### Episode info #####
sub_file = "test.ass"
anime_title = "This anime 9"                       # Book
season = "Season 2"                            # Chapter
episode_title = "Episode 1"                     # Page

# optional for lyrics
upload_lyrics = True
lyrics_only = False
OP_name = "OP_Lyrics"
ED_name = "ED_Lyrics"

# Init lists
script_info = {}
style_info = []
op_lyrics = []
ed_lyrics = []
dialogue = []
log = []
unhandled_lines = False

### Multiple replace
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

sub_dictionary = {
    "{\i1}" : "*", "{\i0}" : "*"
    }

## Separator function for main body
def separator(next_line, type="none", format="none", extra="none"):
    ## Default setting
    if type == "DEFAULT":
        # Speaker
        if extra == "flashback":
            speaker = "**(Flashback) " + next_line.split(",")[4] + "**<br>"
        else:
            speaker = "**" + next_line.split(",")[4] + "**<br>"
            
        ## FORMAT: &nbsp;&nbsp;&nbsp;&nbsp;this is a line<br>
        ## For multiline
        if len(next_line.split(",", 9)[9].rstrip().split("\\N")) >= 2:
            separate_lines = []
            for text in next_line.split(",", 9)[9].split("\\N"):
                temp_line = text.rstrip()
                if format == "italics":
                    separate_lines.append("&nbsp;&nbsp;&nbsp;&nbsp;*" + temp_line + "*<br>")
                else:
                    separate_lines.append("&nbsp;&nbsp;&nbsp;&nbsp;" + temp_line + "<br>")
            joined_line = "".join(separate_lines)
            this_line = replace_all(joined_line, sub_dictionary)
            if "{" in this_line:
                log.append("Unhandled line: " + this_line + "\n")
            dialogue.append(speaker + this_line)
        else:
        ## For single line
            temp_line = next_line.split(",", 9)[9].rstrip().split("\\N")[0]
            if format == "italics":
                prep_line = "&nbsp;&nbsp;&nbsp;&nbsp;*" + temp_line + "*<br>"
            else:
                prep_line = "&nbsp;&nbsp;&nbsp;&nbsp;" + temp_line + "<br>"
            this_line = replace_all(prep_line, sub_dictionary)
            if "{" in this_line:
                log.append("Unhandled line: " + this_line + "\n")
            dialogue.append(speaker + this_line)
    
    ## For song lyrics (present as is with <br> between lines)
    elif type == "LYRICS":
        if extra == "OP":
            op_lyrics.append(next_line.split(",", 9)[9].rstrip())
        if extra == "ED":
            ed_lyrics.append(next_line.split(",", 9)[9].rstrip())
        if extra == "EXTRA":
            pass
    
    elif type == "SIGNS":
        this_line = next_line.split(",",9)[9].split("}")[1].replace("\\N", " ")
        dialogue.append("***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;" + str(this_line) + "<br>")
    
    # If unhandled
    else:
        print("Unhandled line: " + mode + " " + next_line.split(",", 9)[4] + " " + next_line.split(",", 9)[9])
        log.append("Unhandled line: " + mode + " " + next_line.split(",", 9)[4] + " " + next_line.split(",", 9)[9])


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
with open(sub_file, "r", encoding="utf8") as file:
    ## Loop for metadata-type data (Script Info)
    file.readline()
    while True:
        next_line = file.readline()
        
        if not next_line:
            break
        elif next_line == "[V4+ Styles]\n":
#             print("Styles")
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
#             print("Events")
            break
        if next_line == "[Events]\n" or next_line == "\n" or next_line == "Format:\n" or next_line == "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,Strikeout,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n":
            pass
        else:
            style_info.append(next_line.split(",")[0].split(": ")[1])
        
        
    
    ## Start another loop for dialogue events (Events). Uses separator
    while True:
        next_line = file.readline()
        if not next_line:
            break
        
        mode = next_line.split(",")[3]
        
        if mode == "Songs_OP":
            separator(next_line, type="LYRICS", extra="OP")      
        elif mode == "Songs_ED":
            separator(next_line, type="LYRICS", extra="ED")     
        elif "Default" in mode:
            if mode == "DefaultItalics":
                separator(next_line, type="DEFAULT", format="italics")
            else:
                separator(next_line, type="DEFAULT")
        elif "Flashback" in mode:
            separator(next_line, type="DEFAULT", extra="flashback")
        elif "Signs" in mode:
            separator(next_line, type="SIGNS")
        
        # Catches unhandled lines
        else:
            separator(next_line)

for text in log: 
    if "Unhandled line:" in text:
        unhandled_lines = True
        print("Upload aborted. Check log for unhandled lines.")
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
with open('dumps/dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(full_dialogue))

## Lyrics
op_lyrics_full = "<br>".join(op_lyrics)
ed_lyrics_full = "<br>".join(ed_lyrics)

with open('dumps/op_dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(op_lyrics_full))
    
with open('dumps/ed_dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(ed_lyrics_full))


####################################
## FULL API SEQUENCE
if not unhandled_lines:
## Book search and create
#     Init vars
    BOOK_ID = 0
    found = False
    todo = ""

    response = requests.get(secrets['book_url'], headers=headers)
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
    found = False

    response = requests.get(secrets['chapter_url'], headers=headers)
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
        # OP
        todo = {
            "book_id": BOOK_ID,
            "chapter_id": CHAPTER_ID,
            "name": OP_name,
            "markdown": op_lyrics_full
            }
        response = requests.post(secrets['page_url'], json=todo, headers=headers)
        log.append(str(response.status_code) + " " + OP_name + " added\n")
        
        # ED
        todo = {
            "book_id": BOOK_ID,
            "chapter_id": CHAPTER_ID,
            "name": ED_name,
            "markdown": ed_lyrics_full
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
    
with open('dumps/log.txt', 'w', encoding="utf8") as f:
    f.write(log_full)
# 
print("DONE " + str(lines))
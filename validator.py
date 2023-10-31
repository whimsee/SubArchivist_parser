import json
import requests
import re

episodes = []
source_links = []

### Easy info from local links.json (same folder as .py file) ###
with open("links.json", 'r', encoding="utf8") as file:
    data = json.load(file)
    link_title = data['title'].replace(" ","_").replace("'","\'").replace(":","").replace(";", "_")
    link_season = data['season'].replace(" ","_")
    for x, y in data['episodes'].items():    
        episodes.append(x)
        source_links.append(y)

##### Episode info #####
        ### MANUAL ####
# episode_title = "E7 - Shooting Star Moratorium"         # Page
# anime_title = "Laid-Back Camp"                       # Book
# season = "Season 2"                            # Chapter
# source_link = "https://www.crunchyroll.com/watch/G63K48VZ6/shooting-star-moratorium"

### Automatic (based on local links.json) ###
index = 0    # Starts from 0
episode_title = episodes[index]
file_name = episode_title.replace(" ","_").replace(":","-").replace("?","").replace("("," ").replace(")"," ")
sub_file = "subs/" + link_title + "/" + link_season + "/" + file_name + ".ass"
anime_title = data['title']
season = data['season']
source = "Crunchyroll"               # Feel free to change if from another official source
source_link = source_links[index]

print("Checking", episode_title)

## Name replace dictionary (based on name_dict.json from the source .ass folder)
with open("subs/" + link_title + "/" + link_season + "/name_dict.json") as json_data:
    name_dict = json.load(json_data)

# optional for lyrics (Unused for checker)
upload_lyrics = False
insert_song = False
lyrics_only = False
op_only = False
ed_only = False
OP_name = "OP - SOUVENIR"
ED_name = "ED - Bokura Dake no Shudaika"
Insert_name = "Yoru ga Akeru" 

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

    if "{\i1}" in text and not "{\i0}" in text:
        if not "{\i}" in text:
            text = text.rstrip() + "{\i0}"
    elif "{\i0}" in text and not "{\i1}" in text:
        text = text.strip("{\i0}")

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
    "{\\an2\i1}" : "{\\i1}",
    "{\\an8\i1}" : "{\\i1}",
    "{\i}\\N" : "{\i}<br>\n&nbsp;&nbsp;&nbsp;&nbsp;",
    "\\N": "<br>\n&nbsp;&nbsp;&nbsp;&nbsp;"
    }

def clean_text(text):
    if any(s in text for s in ("{", "}")):
        temp_text = replace_all(text, sub_dictionary)
        sub_text = re.sub("[\{\[].*?[\}\]]", "", temp_text)
        this_line = sub_text.replace("\\N", " ").replace("\\n", " ")
#         print(this_line)
        return this_line
    else:
        return text

### Separator function for main body
def separator(next_line, type="none", format="none", extra="none"):
    
    # Speaker
    if not type == "SIGNS":
        temp_speaker = replace_name(next_line.split(",")[4], name_dict, next_line.split(",")[1])
            
    # Cleaned text. Only keep inline italics.        
    base_text = clean_text(next_line.split(",", 9)[9])
    
    ## Default setting
    if type == "DEFAULT":
        ## FORMAT: &nbsp;&nbsp;&nbsp;&nbsp;this is a line<br>
        ## For multiline
        if len(base_text.rstrip().split("\\N")) >= 2:
            pass
        else:
        ## For single line
            pass
    
    ## For song lyrics (present as is with <br> between lines)
    elif type == "LYRICS":
        pass
    
    elif type == "SIGNS":
        pass
    
    # If unhandled
    else:
        print("Unhandled line: " + next_line.split(",", 9)[1] + " " + mode + " " + next_line.split(",", 9)[4] + " " + base_text)
        log.append("Unhandled line: " + next_line.split(",", 9)[1] + " " + mode + " " + next_line.split(",", 9)[4] + " " + base_text)

### Main Loop ###############################################################################################
with open(sub_file, "r", encoding="utf8") as file:
    
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
        next_line = file.readline()
        if not next_line:
            break
        
        mode = next_line.split(",")[3].lower()
        agent = next_line.split(",")[4].lower()
        
        if mode == "songs_op":
            separator(next_line, type="LYRICS", extra="OP")      
        elif mode == "songs_ed":
            separator(next_line, type="LYRICS", extra="ED")
        elif mode == "songs_insert":
            separator(next_line, type="LYRICS", extra="EXTRA")
        elif any(s in mode for s in ("default", "main", "top", "bd dx", "dx", "top dx")):
            if any(s in agent for s in (
                "sign", "board", "desk", "note", "book", "text", "paper",
                "tape", "title", "nameplate", "notice", "sheet", "calendar",
                "phone screen", "building", "exhibition", "phone", "leaflet",
                "wall", "screen", "slate"
                )):
                separator(next_line, type="SIGNS")
            elif "italics" in mode:
                separator(next_line, type="DEFAULT", format="italics")
            else:
                separator(next_line, type="DEFAULT")
        elif "italics" in mode:
            separator(next_line, type="DEFAULT", format="italics")
        elif "texting" in mode:
            separator(next_line, type="DEFAULT", extra="texting")
        elif "messenger" in mode:
            separator(next_line, type="DEFAULT", extra="messenger")
        elif "phone" in mode:
            separator(next_line, type="DEFAULT", extra="messenger")
        elif "flashback" in mode:
            separator(next_line, type="DEFAULT", extra="flashback")
        elif any(s in mode for s in ("sign", "next ep", "ep title", "generic caption", "fromhere", "sine", "title", "setting")):
            separator(next_line, type="SIGNS")
        
        # Catches unhandled lines
        else:
            separator(next_line)

## Check for unhandled lines and aborts upload
for text in log: 
    if "Unhandled line:" in text:
        unhandled_lines = True
        print("Check log for unhandled lines.")
        break
    
    if "Unhandled name:" in text:
        unhandled_lines = True
        print("Check log for unhandled names.")
        break

### Joining arrays for dumps ###########################
## Dialogue

## Lyrics

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
    
with open('dumps/' + anime_title + '-' + file_name + '-log.txt', 'w', encoding="utf8") as f:
    f.write(log_full)
#
if unhandled_lines:
    print("DONE!")
else:
    print("PASS!")
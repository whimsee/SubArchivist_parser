# import ftfy
# import re
import json

script_info = {}
style_info = {}
op_lyrics = []
ed_lyrics = []
dialogue = []
log = []

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
            this_line = "".join(separate_lines)
            dialogue.append(speaker + this_line)
        else:
        ## For single line
            temp_line = next_line.split(",", 9)[9].rstrip().split("\\N")[0]
            if format == "italics":
                this_line = "&nbsp;&nbsp;&nbsp;&nbsp;*" + temp_line + "*<br>"
            else:
                this_line = "&nbsp;&nbsp;&nbsp;&nbsp;" + temp_line + "<br>"
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
#             print(this_line)
        dialogue.append("***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;" + str(this_line) + "<br>")
    
    # If unhandled
    else:
        print("Unhandled line: " + mode + " " + next_line.split(",", 9)[4] + " " + next_line.split(",", 9)[9])
        log.append("Unhandled line: " + mode + " " + next_line.split(",", 9)[4] + " " + next_line.split(",", 9)[9])

### Main Loop
with open("test.ass", "r", encoding="utf8") as file:
    ## Loop for metadata-type data (Script Info)
    file.readline()
    while True:
        next_line = file.readline()
        
        if not next_line:
            break
        elif next_line == "[V4+ Styles]\n":
            print("Styles")
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
            print("Events")
            break
        
        if next_line == "[Events]\n":
            pass
        
        
    
    ## Start another loop for dialogue events (Events)
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

# For debug
# dump_dialogue = "\n".join(dialogue)
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

## Joining arrays for dumps

# Dialogue
dump_dialogue = "".join(dialogue)

with open('dumps/dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(dump_dialogue))

# Lyrics
op_lyrics_full = "<br>".join(op_lyrics)
ed_lyrics_full = "<br>".join(ed_lyrics)

with open('dumps/op_dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(op_lyrics_full))
    
with open('dumps/ed_dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(ed_lyrics_full))

# Handle log
lines = len(dialogue)
for x, y in script_info.items():
    log_text = x + ": " + y
    log.append(log_text)

log.append("\n")
log.append(str(lines) + " lines")
log_full = "".join(log)
    
with open('dumps/log.txt', 'w', encoding="utf8") as f:
    f.write(log_full)

print("DONE " + str(lines))
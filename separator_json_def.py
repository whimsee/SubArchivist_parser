# import ftfy
# import re
import json

text_extract = {}
op_lyrics = []
ed_lyrics = []
dialogue = []

def separator(next_line, type="DEFAULT", format="none", extra="none"):
    
    if type == "DEFAULT":
        if extra == "flashback":
            speaker = "**(Flashback) " + next_line.split(",")[4] + "**<br>"
        else:
            speaker = "**" + next_line.split(",")[4] + "**<br>"
            
        # FORMAT: &nbsp;&nbsp;&nbsp;&nbsp;this is the first line<br>
        if len(next_line.split(",", 9)[9].rstrip().split("\\N")) >= 2:
            separate_lines = []
            for text in next_line.split(",", 9)[9].split("\\N"):
                temp_line = text.rstrip()
                if format == "italics":
                    separate_lines.append("&nbsp;&nbsp;&nbsp;&nbsp;*" + temp_line + "*<br>")
                else:
                    separate_lines.append("&nbsp;&nbsp;&nbsp;&nbsp;" + temp_line + "<br>")
            this_line = "".join(separate_lines)
#             print(this_line)
            dialogue.append(speaker + this_line)
        else:
            temp_line = next_line.split(",", 9)[9].rstrip().split("\\N")[0]
            if format == "italics":
                this_line = "&nbsp;&nbsp;&nbsp;&nbsp;*" + temp_line + "*<br>"
            else:
                this_line = "&nbsp;&nbsp;&nbsp;&nbsp;" + temp_line + "<br>"
#             print(this_line)
            dialogue.append(speaker + this_line)

with open("test.ass", "r", encoding="utf8") as file:
    # Loop for metadata-type data
    while True:
        this_line = ""
        next_line = file.readline()
        
        if not next_line:
            break
        
        if "Original Script" in next_line:
            this_line = next_line.split(": ")[1].split("  [")[0]
            text_extract.update({"Original_Script" : this_line})
        
        if next_line == "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n":
            break
    
    ## Start another loop for dialogue events
    while True:
        next_line = file.readline()
        if not next_line:
            break
        
#         print(next_line.split(",")[3])
        
        if next_line.split(",")[3] == "Songs_OP":
            op_lyrics.append(next_line.split(",", 9)[9].rstrip())
            
        if next_line.split(",")[3] == "Songs_ED":
            ed_lyrics.append(next_line.split(",", 9)[9].rstrip())
            
        if "Default" in next_line.split(",")[3]:
            if next_line.split(",")[3] == "DefaultItalics":
                separator(next_line, format="italics")
            else:
                separator(next_line)
        
        if "Flashback" in next_line.split(",")[3]:
            separator(next_line, extra="flashback")
#             print("FLASHBACK")
# #             print(next_line.split(",")[4])
# #             print(next_line.split(",", 9)[9].rstrip().split(" \\N"))
#             speaker = next_line.split(",")[4]
#             if len(next_line.split(",", 9)[9].rstrip().split(" \\N")) >= 2:
#                 separate_lines = next_line.split(",", 9)[9].rstrip().split(" \\N")
#                 this_line = "\n".join(separate_lines)
#                 dialogue.append("F " + speaker + " " + this_line)
#             else:
#                 this_line = next_line.split(",", 9)[9].rstrip().split(" \\N")
#                 dialogue.append("F " + speaker + " " + this_line[0])
#             
#         if "Signs" in next_line.split(",")[3]:
#             print("SIGNS")
#             this_line = next_line.split(",",9)[9].split("}")[1].replace("\\N", " ")
# #             print(this_line)
#             dialogue.append("S " + str(this_line))

# For debug
# dump_dialogue = "\n".join(dialogue)
# for text in dialogue:
#     print(text)

# For production
dump_dialogue = "".join(dialogue)


with open('dumps/dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(dump_dialogue))
#         next_line.strip()

# print(this_line)
 
# print(op_lyrics)
# print(ed_lyrics)

op_lyrics_full = "<br>".join(op_lyrics)
ed_lyrics_full = "<br>".join(ed_lyrics)


with open('dumps/op_dump.txt', 'w', encoding="utf8") as f:
    f.write(op_lyrics_full)
    
with open('dumps/ed_dump.txt', 'w', encoding="utf8") as f:
    f.write(ed_lyrics_full)

# op_lyrics_full = ftfy.fix_encoding("\n".join(op_lyrics))
# ed_lyrics_full = ftfy.fix_encoding("\n".join(ed_lyrics))

# print(op_lyrics_full)
# print("---------")
# print(ed_lyrics_full)
# text_extract.update({"ed_lyrics" : ed_lyrics_full})
# print(text_extract)
print("DONE")
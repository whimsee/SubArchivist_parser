# import ftfy
# import re

text_extract = {}
op_lyrics = []
ed_lyrics = []
dialogue = []

with open("test.ass", "r", encoding="utf8") as file:
    while True:
        next_line = file.readline()
#         print(next_line)
        
        if not next_line:
            break
        
        if "Original Script" in next_line:
            this_line = next_line.split(": ")[1].split("  [")[0]
            text_extract.update({"Original_Script" : this_line})
        
#         next_line.split(",")
#         print(next_line)
        
        if next_line == "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n":
            break
    
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
            print("DEFAULT")
#             print(next_line.split(",")[4])
            print(next_line.split(",", 9)[9].split("\\N"))
            print(len(next_line.split(",", 9)[9].rstrip().split("\\N")))
        
        if "Flashback" in next_line.split(",")[3]:
            print("FLASHBACK")
#             print(next_line.split(",")[4])
#             print(next_line.split(",", 9)[9].rstrip())
            
        if "Signs" in next_line.split(",")[3]:
            print("SIGNS")
            this_line = next_line.split(",",9)[9].split("}")[1].replace("\\N", " ")
            print(this_line)
            
        
#         next_line.strip()

# print(this_line)
 
# print(op_lyrics)
# print(ed_lyrics)

op_lyrics_full = "\n".join(op_lyrics)
ed_lyrics_full = "\n".join(ed_lyrics)

# op_lyrics_full = ftfy.fix_encoding("\n".join(op_lyrics))
# ed_lyrics_full = ftfy.fix_encoding("\n".join(ed_lyrics))
print(op_lyrics_full)
print("---------")
print(ed_lyrics_full)
text_extract.update({"ed_lyrics" : ed_lyrics_full})
# print(text_extract)
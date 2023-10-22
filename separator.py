import ftfy

text_extract = {}
op_lyrics = []
ed_lyrics = []

with open("test.ass", "r") as file:
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
        
        if not next_line:
            break
        
        if "OP LYRICS" in next_line:
            op_lyrics.append(next_line.split(",", 9)[9].strip("\n"))
            
        if "ED LYRICS" in next_line:
            ed_lyrics.append(next_line.split(",", 9)[9].strip("\n"))
        
#         next_line.strip()

# print(this_line)

print(op_lyrics)
print(ed_lyrics)

op_lyrics_full = ftfy.fix_encoding("\n".join(op_lyrics))
ed_lyrics_full = ftfy.fix_encoding("\n".join(ed_lyrics))
print(op_lyrics_full)
print("---------")
print(ed_lyrics_full)
text_extract.update({"ed_lyrics" : op_lyrics_full})
print(text_extract)
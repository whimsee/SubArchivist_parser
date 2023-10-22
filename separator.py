import ftfy

text_extract = {}
op_lyrics = []
ed_lyrics = []

with open("test.ass", "r") as file:
    while True:
        next_line = file.readline()
        print(next_line)
        
        if not next_line:
            break
        
        if "Original Script" in next_line:
            this_line = next_line.split(": ")[1].split("  [")[0]
            text_extract.update({"Original Script" : this_line})
        
        if next_line == "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n":
            print("NEW LOOP")
            break
    

    while True:
        next_line = file.readline()
#         next_line.split(",")
#         print(next_line)
        
        if not next_line:
            break
        
        if "OP LYRICS" in next_line:
            print("OP LYRICS")
            op_lyrics.append(next_line.split(",", 9)[9].strip("\n"))
            
        if "ED LYRICS" in next_line:
            print("ED LYRICS")
            ed_lyrics.append(next_line.split(",", 9)[9].strip("\n"))
        
        next_line.strip()

# print(this_line)
# print(text_extract)
print(op_lyrics)
print(ed_lyrics)

op_lyrics_full = "\n".join(op_lyrics)
ed_lyrics_full = "\n".join(ed_lyrics)
print(ftfy.fix_encoding(op_lyrics_full))
print("---------")
print(ftfy.fix_encoding(ed_lyrics_full))
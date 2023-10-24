import json
# with open("links.json", 'r', encoding="utf8") as file:
#     while True:
#         next_line = file.readline()
# 
#         if not next_line:
#             break;
#         links.append(next_line.strip())
#     
# for link in links:
#     print (link)

with open("links.json", 'r', encoding="utf8") as file:
    data = json.load(file)
    print(data)
    
    for x, y in data.items():
        print(x, y)
    
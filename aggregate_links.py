links = []
with open("links.txt",'r') as file:
    while True:
        next_line = file.readline()

        if not next_line:
            break;
        links.append(next_line.strip())
    
for link in links:
    print (link)
file = open("links.txt",'r')
links = []

while True:
    next_line = file.readline()

    if not next_line:
        break;
    links.append(next_line.strip())
    
file.close()
for link in links:
    print (link)
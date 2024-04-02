from os import walk

def sort_key(title_temp):
    number_temp = []
    for i in range(5):
        digit = title_temp[i]
        if digit.isdigit():
            number_temp.append(digit)
        else:
            pass
    if len(number_temp) < 2:
        number_temp.insert(0,"0")
    number = "".join(number_temp)
    print(number)
    return int(number)

mypath = "."

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break

f.sort(key=sort_key)
print(f)

# for title in f:
#     number_temp = []
#     print(title)
#     for i in range(5):
#         digit = title[i]
#         if title[i].isdigit():
#             number_temp.append(digit)
#         else:
#             pass
#     if len(number_temp) < 2:
#         number_temp.insert(0,"0")
#     number = "".join(number_temp)
#     print(number)
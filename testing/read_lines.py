import subprocess

process = subprocess.run('date', shell=True,text=True, capture_output=True)

print(process)

# open the data file
file = open("test.ass")
# read the file as a list
data = file.readlines()
# close the file
file.close()

print(data)
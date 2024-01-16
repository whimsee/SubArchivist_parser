import subprocess
output = subprocess.getoutput('crunchy-cli search "https://www.crunchyroll.com/watch/GY4PVN036/prologue" --audio ja-JP -o {{episode.title}}')
print (output)
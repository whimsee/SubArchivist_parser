import subprocess
output = subprocess.getoutput('crunchy-cli search "https://www.crunchyroll.com/watch/GY8DEQ5GY/behind-the-scenes-of-chihayafuru" --audio ja-JP -o "{{episode.title}} {{episode.sequence_number}}"')
print (output)
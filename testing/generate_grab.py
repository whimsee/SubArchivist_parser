import pycurl
import certifi
from io import BytesIO
import json
from pathlib import Path
import subprocess
import shutil
import re




# crunchy-cli search --audio ja-JP -o '{{episode.sequence_number}} - {{episode.title}} - {{subtitle.locale}} - {{subtitle.url}}' https://www.crunchyroll.com/series/G6QWDD096/magia-record-puella-magi-madoka-magica-side-story\[S1\] | grep "en-US"

episodes = subprocess.getoutput('crunchy-cli search --audio ja-JP -o "{{episode.sequence_number}} - {{episode.title}} - {{subtitle.locale}} - {{subtitle.url}}" https://www.crunchyroll.com/series/G6QWDD096/magia-record-puella-magi-madoka-magica-side-story[S1] | grep "en-US"')
episode_list = episodes.split("\n")

print(len(episode_list))



for eps in episode_list:
    episode_number = eps.split(" - ")[0]
    episode_title = eps.split(" - ")[1]
    print(episode_number, episode_title)
# print(episode_list[1].split(" - ")[3])

# buffer = BytesIO()
# c = pycurl.Curl()
# c.setopt(c.URL, link)
# c.setopt(c.WRITEDATA, buffer)
# c.setopt(c.CAINFO, certifi.where())
# c.perform()
# c.close()
# 
# body = buffer.getvalue()
# # Body is a byte string.
# # We have to know the encoding in order to print it to a text file
# # such as standard output.
# print(body.decode('utf-8'))
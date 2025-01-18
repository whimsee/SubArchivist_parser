import pycurl
from io import BytesIO

import json
from pathlib import Path
import subprocess
import shutil
import re
import sys
from enum import Enum


#set up variables
body = BytesIO()
connection = pycurl.Curl()

link = "https://www.crunchyroll.com/watch/GD9UV83MG/why-dont-you-go-for-a-ride"
audio = "ja-JP"
link_type = "E"

episode_name = subprocess.getoutput('crunchy-cli search "' +  link + '" --audio ' + audio + ' -o ' + link_type + '"{{episode.sequence_number}} - {{episode.title}}"').replace(r"\N","")

print(episode_name)

# subprocess.run("curl -o subs/" + link_title + "/" + folder_season + "/" + file_name + ".ass $(crunchy-cli search --audio " + audio + " -o '{{subtitle.locale}} {{subtitle.url}}' " + link + " | grep 'en-US' | awk '{print $2}')", shell=True)

sub_link = subprocess.getoutput("crunchy-cli search --audio '"
                                + audio +
                                "' -o '{{subtitle.locale}} {{subtitle.url}}' '"
                                + link +
                                "' | grep 'en-US' | awk '{print $2}'")
print(sub_link)

connection = pycurl.Curl()
connection.setopt(connection.URL, sub_link)

#write data to the output variable
connection.setopt(connection.WRITEDATA, body)

#run the command
connection.perform()

#end the session
connection.close()

#extract the response body from the output variable
sub_file = body.getvalue().decode('utf-8')
print(sub_file)

with open('curl.txt','w', encoding="utf8") as f:
    f.write(sub_file)
# ok
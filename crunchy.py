import subprocess
links = ("https://www.crunchyroll.com/watch/G6K5K9Z7Y/kotoura-san-and-manabe-kun","https://www.crunchyroll.com/watch/GR>
for link in links:
    print (subprocess.check_output("curl $(crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}>
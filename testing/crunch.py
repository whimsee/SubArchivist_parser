import subprocess
links = ("https://www.crunchyroll.com/watch/G6K5K9Z7Y/kotoura-san-and-manabe-kun","https://www.crunchyroll.com/watch/GR49GVW86/but-youre-not-here")

for link in links:
	print (subprocess.check_output("crunchy-cli search --audio ja-JP -o '{{subtitle.locale}} {{subtitle.url}}' " + link + " | grep 'en-US' | awk '{print $2}'", shell=True, text=True))


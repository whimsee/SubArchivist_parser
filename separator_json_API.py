import json
from secrets import secrets
import requests

headers = {"Authorization": "Token " + secrets['API_ID_TOKEN']}

##### Episode info #####
anime_title = "This anime 5"                       # Book
season = "Season 1"                            # Chapter
episode_title = "Episode 2"                     # Page

# optional for lyrics
upload_lyrics = True
lyrics_only = False
OP_name = "OP_Lyrics"
ED_name = "ED_Lyrics"

# Init lists
script_info = {}
style_info = []
op_lyrics = []
ed_lyrics = []
dialogue = []
log = []
unhandled_lines = False

## Separator function for main body
def separator(next_line, type="none", format="none", extra="none"):
    ## Default setting
    if type == "DEFAULT":
        # Speaker
        if extra == "flashback":
            speaker = "**(Flashback) " + next_line.split(",")[4] + "**<br>"
        else:
            speaker = "**" + next_line.split(",")[4] + "**<br>"
            
        ## FORMAT: &nbsp;&nbsp;&nbsp;&nbsp;this is a line<br>
        ## For multiline
        if len(next_line.split(",", 9)[9].rstrip().split("\\N")) >= 2:
            separate_lines = []
            for text in next_line.split(",", 9)[9].split("\\N"):
                temp_line = text.rstrip()
                if format == "italics":
                    separate_lines.append("&nbsp;&nbsp;&nbsp;&nbsp;*" + temp_line + "*<br>")
                else:
                    separate_lines.append("&nbsp;&nbsp;&nbsp;&nbsp;" + temp_line + "<br>")
            this_line = "".join(separate_lines)
            dialogue.append(speaker + this_line)
        else:
        ## For single line
            temp_line = next_line.split(",", 9)[9].rstrip().split("\\N")[0]
            if format == "italics":
                this_line = "&nbsp;&nbsp;&nbsp;&nbsp;*" + temp_line + "*<br>"
            else:
                this_line = "&nbsp;&nbsp;&nbsp;&nbsp;" + temp_line + "<br>"
            dialogue.append(speaker + this_line)
    
    ## For song lyrics (present as is with <br> between lines)
    elif type == "LYRICS":
        if extra == "OP":
            op_lyrics.append(next_line.split(",", 9)[9].rstrip())
        if extra == "ED":
            ed_lyrics.append(next_line.split(",", 9)[9].rstrip())
        if extra == "EXTRA":
            pass
    
    elif type == "SIGNS":
        this_line = next_line.split(",",9)[9].split("}")[1].replace("\\N", " ")
        dialogue.append("***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;" + str(this_line) + "<br>")
    
    # If unhandled
    else:
        print("Unhandled line: " + mode + " " + next_line.split(",", 9)[4] + " " + next_line.split(",", 9)[9])
        log.append("Unhandled line: " + mode + " " + next_line.split(",", 9)[4] + " " + next_line.split(",", 9)[9])


def API_get(target, type="list", ID=0):
    
    if type == "list":
        if target == "book":
            response = requests.get(secrets['book_url'], headers=headers)
        elif target == "chapter":
            response = requests.get(secrets['chapter_url'], headers=headers)
        elif target == "page":
            response = requests.get(secrets['page_url'], headers=headers)
        
        return(response.json())
    
    if type == "read":
        if target == "book":
            response = requests.get(secrets['book_url'] + str(ID), headers=headers)
        elif target == "chapter":
            response = requests.get(secrets['chapter_url'] + str(ID), headers=headers)
        elif target == "page":
            response = requests.get(secrets['page_url'] + str(ID), headers=headers)
        
        return(response.json())
        
### Main Loop ###############################################################################################
with open("test.ass", "r", encoding="utf8") as file:
    ## Loop for metadata-type data (Script Info)
    file.readline()
    while True:
        next_line = file.readline()
        
        if not next_line:
            break
        elif next_line == "[V4+ Styles]\n":
#             print("Styles")
            break
        
        if "Original Script" in next_line:
            this_line = next_line.split(": ")[1].split("  [")[0]
            script_info.update({"Original_Script" : this_line + "\n"})
        elif next_line == "\n":
            pass
        else:
            this_line = next_line.split(": ")
            try:
                script_info.update({this_line[0] : this_line[1]})
            except IndexError:
                script_info.update({this_line[0] : "\n"})
    
    ## Start another loop for Styles
    while True:
        next_line = file.readline()
        
        if not next_line:
            break
        elif next_line == "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n":
#             print("Events")
            break
        if next_line == "[Events]\n" or next_line == "\n" or next_line == "Format:\n" or next_line == "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,Strikeout,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n":
            pass
        else:
            style_info.append(next_line.split(",")[0].split(": ")[1])
        
        
    
    ## Start another loop for dialogue events (Events). Uses separator
    while True:
        next_line = file.readline()
        if not next_line:
            break
        
        mode = next_line.split(",")[3]
        
        if mode == "Songs_OP":
            separator(next_line, type="LYRICS", extra="OP")      
        elif mode == "Songs_ED":
            separator(next_line, type="LYRICS", extra="ED")     
        elif "Default" in mode:
            if mode == "DefaultItalics":
                separator(next_line, type="DEFAULT", format="italics")
            else:
                separator(next_line, type="DEFAULT")
        elif "Flashback" in mode:
            separator(next_line, type="DEFAULT", extra="flashback")
            separator(next_line, extra="flashback")
        elif "Signs" in mode:
            separator(next_line, type="SIGNS")
        
        # Catches unhandled lines
        else:
            separator(next_line)

for text in log: 
    if "Unhandled line:" in text:
        unhandled_lines = True
        print("Upload aborted. Check log for unhandled lines.")
        break


#### For debug
# dump_dialogue = "\n".join(dialogue)
# for text in dialogue:
#     print(text)

# print(this_line)
# print(op_lyrics)
# print(ed_lyrics)

# print(op_lyrics_full)
# print("---------")
# print(ed_lyrics_full)
# text_extract.update({"ed_lyrics" : ed_lyrics_full})
# print(script_info)

### Joining arrays for dumps ###########################

## Dialogue
dump_dialogue = "".join(dialogue)

with open('dumps/dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(dump_dialogue))

## Lyrics
op_lyrics_full = "<br>".join(op_lyrics)
ed_lyrics_full = "<br>".join(ed_lyrics)

with open('dumps/op_dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(op_lyrics_full))
    
with open('dumps/ed_dump.txt', 'w', encoding="utf8") as f:
    f.write(json.dumps(ed_lyrics_full))


####################################
## FULL API SEQUENCE
if not unhandled_lines:
## Book search and create
#     Init vars
    BOOK_ID = 0
    found = False
    todo = ""

    response = requests.get(secrets['book_url'], headers=headers)
    list = response.json()

    for data in list['data']:
        if anime_title in data['name']:
            BOOK_ID = data['id']
            found = True
            log.append("Anime: " + data['name'] + "\n")
            break
    if not found:
        # add to log
        log.append("Anime not found. Creating " + anime_title + "\n")
        todo = {
            "name": anime_title,
            "description": "If that book isn't here"
        }
        response = requests.post(secrets['book_url'], json=todo, headers=headers)
        BOOK_ID = response.json()['id']
        

    ## Chapter search and create
    todo = ""
    CHAPTER_ID = 0
    found = False

    response = requests.get(secrets['chapter_url'], headers=headers)
    list = response.json()
    for data in list['data']:
        if str(BOOK_ID) in str(data['book_id']):
            if data['name'] == season:
                # add to log
                log.append("Season found\n")
                CHAPTER_ID = data['id']
                found = True
                break

    if not found:
        # add to log
        log.append("Season not found. Adding " + season + "\n")
        todo = {
            "book_id": BOOK_ID,
            "name": season
        }
        response = requests.post(secrets['chapter_url'], json=todo, headers=headers)
        CHAPTER_ID = response.json()['id']

    ## POST PAGE
    todo = ""
    found = False

    if not lyrics_only:
        todo = {
            "book_id": BOOK_ID,
            "chapter_id": CHAPTER_ID,
            "name": episode_title,
            "markdown": "***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;Beyond Journey's End\n<br>***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;At the northernmost end of the continent, I arrived at the place that the people of this world call heaven: Aureole, the land where souls rest.\n<br>***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;Many souls gather there, and I spoke with friends who once fought alongside me. \u2014Flamme the Legendary Mage\n<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Frieren.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;The royal capital's in sight.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;The adventurers are making<br>&nbsp;&nbsp;&nbsp;&nbsp;their triumphant return.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;They must be celebrating in the city.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;We'll have to look for work once we're back.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You're already thinking about that?<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's important, after all.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;We've defeated the Demon King,<br>&nbsp;&nbsp;&nbsp;&nbsp;but it's not over.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;We have the whole rest<br>&nbsp;&nbsp;&nbsp;&nbsp;of our lives ahead of us.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Work, huh?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'd like something where<br>&nbsp;&nbsp;&nbsp;&nbsp;I can drink on the job.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Aren't you a priest?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I suppose you're right.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Frieren, the life ahead of you will surely<br>&nbsp;&nbsp;&nbsp;&nbsp;be much longer than we can imagine.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Perhaps.<br>***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;Beyond Journey's End\n<br>**KING**<br>&nbsp;&nbsp;&nbsp;&nbsp;Himmel the Hero,<br>**KING**<br>&nbsp;&nbsp;&nbsp;&nbsp;Eisen the Warrior, Heiter the Priest,<br>**KING**<br>&nbsp;&nbsp;&nbsp;&nbsp;and Frieren the Mage.<br>**KING**<br>&nbsp;&nbsp;&nbsp;&nbsp;Thank you for defeating the Demon King.<br>**KING**<br>&nbsp;&nbsp;&nbsp;&nbsp;Now our world will enter an age of peace.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;The king's going to erect<br>&nbsp;&nbsp;&nbsp;&nbsp;statues of us in the plaza.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm not sure they'll be able to faithfully<br>&nbsp;&nbsp;&nbsp;&nbsp;recreate my handsome looks, though.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;How self-serving of him.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;He only gave us ten copper coins<br>&nbsp;&nbsp;&nbsp;&nbsp;when we left on our adventure.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Now, now, Frieren.<br>&nbsp;&nbsp;&nbsp;&nbsp;Tonight, we drink for free.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'd say we're even, wouldn't you?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You corrupt priest.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's over.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Yeah.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;This is the end of our adventure.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's been ten years, huh?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;We've been through a lot.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;The day we departed...<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Himmel and Eisen were nearly executed<br>&nbsp;&nbsp;&nbsp;&nbsp;for speaking rudely to the king.<br>**(Flashback) KING**<br>&nbsp;&nbsp;&nbsp;&nbsp;Kill them.<br>**(Flashback) FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;We'll give them a talking to.<br>**(Flashback) HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Shall we lick your boots?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;One misstep, and our adventure<br>&nbsp;&nbsp;&nbsp;&nbsp;would've ended there.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Sometimes, Heiter was too<br>&nbsp;&nbsp;&nbsp;&nbsp;hungover to do anything.<br>**(Flashback) FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You're as pallid as an undead.<br>&nbsp;&nbsp;&nbsp;&nbsp;Are you all right?<br>**(Flashback) HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;No.<br>**(Flashback) HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;No, huh?<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It was a weekly occurrence.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I, on the other hand, was exceptional.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;We thought about leaving you behind<br>&nbsp;&nbsp;&nbsp;&nbsp;when that mimic tried to eat you.<br>**(Flashback) HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Seriously? We told her it was a trap.<br>**(Flashback) FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's dark and scary in here!<br>**(Flashback) EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Why don't we leave the elf behind?<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;We have nothing but terrible memories.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;But I had fun.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm glad I got to adventure with all of you.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Likewise.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It was a mere ten-year adventure.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;\"A mere ten-year adventure\"?<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;But that's an entire decade<br>&nbsp;&nbsp;&nbsp;&nbsp;we spent adventuring together.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Look at Heiter. He's turned into an old man.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;That's rude.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;He always looked like that.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;That's rude.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's nearly time.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;The Era Meteor Shower, was it?<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;It happens once every fifty years.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Perfect for marking the<br>&nbsp;&nbsp;&nbsp;&nbsp;start of an era of peace.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;They're beautiful.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;The view's not so good<br>&nbsp;&nbsp;&nbsp;&nbsp;from inside the city, though.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm having a moment over here.<br>&nbsp;&nbsp;&nbsp;&nbsp;Don't spoil the mood.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Next time, then.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I know a place where you<br>&nbsp;&nbsp;&nbsp;&nbsp;can see them more clearly.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'll take you there in fifty years.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;What?<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's nothing.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;You're right. Let's go see them together.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Well, I should go.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;What are you going to do now?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm going to continue collecting spells.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I plan to travel around the central lands<br>&nbsp;&nbsp;&nbsp;&nbsp;for the next hundred years or so.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'll stop by once in a while.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;I can't understand what<br>&nbsp;&nbsp;&nbsp;&nbsp;being an elf must be like.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Seriously, how long has she been around?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;To her, fifty or even a hundred years<br>&nbsp;&nbsp;&nbsp;&nbsp;might be a trifling thing.<br>**SHOPKEEPER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Shadow dragon horns?<br>**SHOPKEEPER**<br>&nbsp;&nbsp;&nbsp;&nbsp;We don't have those here.<br>**SHOPKEEPER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Haven't seen a shadow dragon<br>&nbsp;&nbsp;&nbsp;&nbsp;in twenty or thirty years.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I see. That's no good.<br>&nbsp;&nbsp;&nbsp;&nbsp;I need one for summoning.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;*Come to think of it, I think Himmel still has*<br>&nbsp;&nbsp;&nbsp;&nbsp;*the horn we got at the Demon King's castle.*<br>**(Flashback) HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's exuding some kind of evil aura.<br>**(Flashback) HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's not harmful to people, is it?<br>**(Flashback) FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I don't know.<br>**(Flashback) HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;You don't know, huh?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;*It's nearly time for the*<br>&nbsp;&nbsp;&nbsp;&nbsp;*Era Meteor Shower again.*<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;*I'll pick the horn up when I visit him.*<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;*The city's changed quite a bit*<br>&nbsp;&nbsp;&nbsp;&nbsp;*since I was last here.*<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It should be around here.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Frieren?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Himmel...<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You're so old.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Do you have to put it so bluntly?<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm still pretty handsome<br>&nbsp;&nbsp;&nbsp;&nbsp;at this age, though, aren't I?<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's been fifty years.<br>&nbsp;&nbsp;&nbsp;&nbsp;You look the same as you ever did.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;I thought I'd never see you again.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;The Era Meteor Shower, huh?<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;That brings back memories.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;About that thing we looted from<br>&nbsp;&nbsp;&nbsp;&nbsp;the Demon King's castle...<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;You mean the shadow dragon horn?<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;I've never forgotten about it.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;My cabinet's been exuding<br>&nbsp;&nbsp;&nbsp;&nbsp;an evil aura all this time.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Sorry, I think.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You could've stashed it<br>&nbsp;&nbsp;&nbsp;&nbsp;in a shed or something.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;I couldn't do that.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;You may not have thought much<br>&nbsp;&nbsp;&nbsp;&nbsp;of leaving it with me,<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;but to me, it was a treasure<br>&nbsp;&nbsp;&nbsp;&nbsp;entrusted to me by a dear friend.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;I had to return it to you someday.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's not that big a deal.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Himmel, are you ready yet?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You're bald, anyway. There's no point<br>&nbsp;&nbsp;&nbsp;&nbsp;in fussing over your appearance.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;There are things we bald men<br>&nbsp;&nbsp;&nbsp;&nbsp;are particular about.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Now, shall we go see the Era Meteor Shower?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You've become rather dignified, Heiter.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm a bishop of the holy city, after all.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;You haven't changed at all.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Don't pat my head.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Eisen, you haven't changed much.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Is that how I seem to you?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I would expect as much from a dwarf.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;So, where's this place where we can<br>&nbsp;&nbsp;&nbsp;&nbsp;see the meteor shower clearly?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;We're going there now?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's a bit early to see the<br>&nbsp;&nbsp;&nbsp;&nbsp;Era Meteor Shower, isn't it?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Yeah. It's about a week's walk from here.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's that far away?<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Unbelievable.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;You should be kinder to the elderly.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;This brings back memories.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Traveling together like this makes me<br>&nbsp;&nbsp;&nbsp;&nbsp;feel like we've returned to those days.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;We journeyed to all sorts of places.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Everything seemed so brilliant and new.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;And you were always there<br>&nbsp;&nbsp;&nbsp;&nbsp;in those beautiful memories.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'd been looking forward to the day<br>&nbsp;&nbsp;&nbsp;&nbsp;when we'd all be together again.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Thank you, Frieren.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Because of you, I had this delightful<br>&nbsp;&nbsp;&nbsp;&nbsp;adventure at the very end.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;They're beautiful.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;I think Himmel was happy.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You think so?<br>**ATTENDANT A**<br>&nbsp;&nbsp;&nbsp;&nbsp;She was one of Mr. Himmel's companions?<br>**ATTENDANT A**<br>&nbsp;&nbsp;&nbsp;&nbsp;I haven't seen her look sad once today.<br>**ATTENDANT B**<br>&nbsp;&nbsp;&nbsp;&nbsp;How heartless.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Now, now! We're not wearing<br>&nbsp;&nbsp;&nbsp;&nbsp;sad expressions, either.<br>**ATTENDANT C**<br>&nbsp;&nbsp;&nbsp;&nbsp;Show some respect, Bishop!<br>**ATTENDANT D**<br>&nbsp;&nbsp;&nbsp;&nbsp;You're heartless!<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;You wound me.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's not like I knew anything about him.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;We only traveled together<br>&nbsp;&nbsp;&nbsp;&nbsp;for a mere ten years.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I knew human lives were short, but...<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Why didn't I try to get to know him better?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Don't pat my head.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;I should return to the holy city.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Let me get a good look at your faces.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;This will probably be<br>&nbsp;&nbsp;&nbsp;&nbsp;the last time I see you.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Are you unwell?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;My years of drinking have caught up to me.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's divine punishment.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;If you're ever in the holy city,<br>&nbsp;&nbsp;&nbsp;&nbsp;offer a drink at my grave.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Heiter, you're not afraid of dying?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;We're the party of adventurers<br>&nbsp;&nbsp;&nbsp;&nbsp;that saved the world.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;We'll surely be living the good life<br>&nbsp;&nbsp;&nbsp;&nbsp;in Heaven after death.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;That's the whole reason<br>&nbsp;&nbsp;&nbsp;&nbsp;I fought alongside you.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You corrupt priest.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;If you'll excuse me.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I should get going, too.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You're off to collect more spells?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;There's that, too,<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;but I want to learn more about humans.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I see.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;So I wanted to ask you something.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Seeing as how I'm a mage, having a powerful<br>&nbsp;&nbsp;&nbsp;&nbsp;warrior to defend me would be a huge help.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Give me a break.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm too old to swing an axe now.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Don't make that face, Frieren.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Surprisingly, life slows down<br>&nbsp;&nbsp;&nbsp;&nbsp;once you've lost your vigor.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I see.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'll see you later, Eisen.<br>**EISEN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Yeah. See you later.<br>***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;Episode 1: The Journey's End\n<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;That's the tree I saw earlier.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I always get lost in these woods.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Where am I?<br>***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;20 years after the death of Himmel the Hero, on the outskirts of the holy city of Strahl in the central lands\n<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Are you looking for something?<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Is something the matter?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm looking for the home<br>&nbsp;&nbsp;&nbsp;&nbsp;of a man named Heiter.<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Then you're a visitor.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You're still alive, you corrupt priest?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Turns out it's harder than I thought<br>&nbsp;&nbsp;&nbsp;&nbsp;to make a stylish exit.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I brought some liquor to offer at your grave.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Would you like a drink?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;I gave up drinking.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I see.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I doubt the Goddess will forgive you<br>&nbsp;&nbsp;&nbsp;&nbsp;even if you clean up your act now.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Thank you.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Who is she?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Her name is Fern.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;She's a war orphan from the southern lands.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's not like you to<br>&nbsp;&nbsp;&nbsp;&nbsp;volunteer to help people.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You're not Himmel, after all.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Frieren, why did you come to visit me?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I was in the holy city<br>&nbsp;&nbsp;&nbsp;&nbsp;picking up some things.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I've been trying to get to know the people<br>&nbsp;&nbsp;&nbsp;&nbsp;I meet on my travels as much as possible.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;And I owe you a lot, so I came to<br>&nbsp;&nbsp;&nbsp;&nbsp;repay my debts before you died.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;In that case, I have a request.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Will you take on an apprentice?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Fern has potential as a mage.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Will you take her with you on your travels?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm sorry, Heiter.<br>&nbsp;&nbsp;&nbsp;&nbsp;That's the one thing I can't do.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;She'd only get in my way.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You know how often<br>&nbsp;&nbsp;&nbsp;&nbsp;apprentice mages die in battle.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm not sending a child my friend<br>&nbsp;&nbsp;&nbsp;&nbsp;asked me to look after to her death.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;I see. Then I have another request.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;This was unearthed from<br>&nbsp;&nbsp;&nbsp;&nbsp;the tomb of Ewig the Sage.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;This grimoire is said to contain lost<br>&nbsp;&nbsp;&nbsp;&nbsp;spells of resurrection and immortality.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I find it hard to believe<br>&nbsp;&nbsp;&nbsp;&nbsp;such magic really exists.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;That's part of why I'd like you to decipher it.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Can you do that?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's written in code using pictures.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;The people of this era<br>&nbsp;&nbsp;&nbsp;&nbsp;really liked this kind of thing.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I could do it, given five or six years.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;I see.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;But why do you want this deciphered?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I thought you weren't afraid of dying.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;I have two reasons.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;The first is that I when I said that,<br>&nbsp;&nbsp;&nbsp;&nbsp;I was just putting on a brave face for you.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;The second is that I'm now more<br>&nbsp;&nbsp;&nbsp;&nbsp;afraid of dying than I was before.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Even if I can't achieve immortality,<br>&nbsp;&nbsp;&nbsp;&nbsp;I'd like a bit more time.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Besides, the holy texts tell us<br>&nbsp;&nbsp;&nbsp;&nbsp;to live healthy lives.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;A long life is the ultimate<br>&nbsp;&nbsp;&nbsp;&nbsp;expression of that, Frieren.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You corrupt priest.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Also, in your spare time,<br>&nbsp;&nbsp;&nbsp;&nbsp;will you teach Fern magic?<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;As a priest, I don't have that knowledge.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I could do that.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;There you are.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I've been looking everywhere for you.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Do you always train in the woods?<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Was finding me difficult even for you?<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Mr. Heiter often tells me<br>&nbsp;&nbsp;&nbsp;&nbsp;I'm practically invisible.<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It's a very good thing, isn't it?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It is.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;*It's true. I can barely detect her mana.*<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;*Her control over her mana is exceptional.*<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;*How much has she studied at such a young age?*<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Mr. Heiter said when I can blast a hole<br>&nbsp;&nbsp;&nbsp;&nbsp;in that rock, I'll be a proper mage.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Oh? Heiter knows what he's<br>&nbsp;&nbsp;&nbsp;&nbsp;talking about. That's\u2014<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;As you just saw, my magic<br>&nbsp;&nbsp;&nbsp;&nbsp;dissipates and doesn't reach it.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;I see.<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;What should I do to train?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Can I ask you something first?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Do you like magic?<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Somewhat.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Just like me, then.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;Is Fern's training coming along smoothly?<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Are you trying to put on<br>&nbsp;&nbsp;&nbsp;&nbsp;a brave face again, Heiter?<br>**HERBALIST**<br>&nbsp;&nbsp;&nbsp;&nbsp;It saddens me to see him treated like this.<br>**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;But they're worth looking for.<br>**HERBALIST**<br>&nbsp;&nbsp;&nbsp;&nbsp;Magic sure is amazing, isn't it?<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;You keep collecting the strangest spells.<br>**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;It'd be a waste for you to die.<br>**HIMMEL**<br>&nbsp;&nbsp;&nbsp;&nbsp;Someday, I'd like to show them to you.<br>***SIGN***&nbsp;&nbsp;&nbsp;&nbsp;Episode 2        It Didn't Have to Be Magic...\n<br>**FERN**<br>&nbsp;&nbsp;&nbsp;&nbsp;It didn't have to be magic...<br>",
        }

        response = requests.post(secrets['page_url'], json=todo, headers=headers)
        # log this
        log.append(str(response.status_code) + " " + episode_title + " added\n")

    if upload_lyrics or lyrics_only:
        # OP
        todo = {
            "book_id": BOOK_ID,
            "chapter_id": CHAPTER_ID,
            "name": OP_name,
            "markdown": "Like a fairy tale<br>It's a sign the story has reached its end<br>Like a single passage taken from<br>A journey that was too long<br>Of the evil that once cast a shadow<br>Across this land<br>And the memories of the short journey<br>With the hero who defeated it<br>The story ends<br>And the hero goes to sleep<br>Leaving this land with<br>Days of peace and quiet<br>The passage of time heartlessly<br>Makes people forget<br>Even the tracks left behind by his life<br>Begin to rust<br>Just the same<br>Your words and wishes and courage<br>Are still inside of me<br>And they live on<br>We chose the same path<br>That's all it was supposed to be<br>Why is it that at some point<br>I wanted to understand the reason for<br>The tears that fall down my cheeks<br>Even now<br>If I retrace the journey we walked together<br>Even though you're not there<br>I know I'll be able to find it"
            }
        response = requests.post(secrets['page_url'], json=todo, headers=headers)
        log.append(str(response.status_code) + " " + OP_name + " added\n")
        
        # ED
        todo = {
            "book_id": BOOK_ID,
            "chapter_id": CHAPTER_ID,
            "name": ED_name,
            "markdown": "And you alright<br>Can you hear me<br>Trailing along deserted train tracks<br>Crying excessively<br>Wanting you to smile<br>I hold on to memories I'd like to keep fresh<br>There's something I'd like to tell you<br>With words more precious than a goodbye<br>Unremarkable yet special<br>See, things that couldn't have been<br>Seen if it weren't for these eyes<br>Why? They begin to overflow<br>So, if I were to be born again<br>I would surely choose this place once more<br>So, if we were to meet again<br>I'd never let you go, I'd choose the present<br>Even if no promises were made<br>Even if I'm lost in days of loneliness<br>Those tears will be alright, \\Ndawn will surely break<br>I\u2019m whispering our lullaby<br>for you to come back home"
            }
        response = requests.post(secrets['page_url'], json=todo, headers=headers)
        log.append(str(response.status_code) + " " + ED_name + " added\n")

## Handle log
lines = len(dialogue)
for x, y in script_info.items():
    log_text = x + ": " + y
    log.append(log_text)

log.append("\n")
log.append("\n".join(style_info))
log.append("\n")
log.append("\n")
log.append(str(lines) + " lines")
log_full = "".join(log)
    
with open('dumps/log.txt', 'w', encoding="utf8") as f:
    f.write(log_full)
# 
print("DONE " + str(lines))
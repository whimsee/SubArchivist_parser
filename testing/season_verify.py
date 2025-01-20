import json
from json import JSONDecodeError
import requests
import re
import sys
import os

from secrets_prod import secrets
headers = {"Authorization": "Token " + secrets['API_ID_TOKEN']}

def verify_season(season_length):

    BOOK_ID = 0
    CHAPTER_ID = 0
    
    response = requests.get(secrets['book_url']+"?count=300&sort=-created_at", headers=headers)
    list = response.json()

    try:
        for data in list['data']:
            if anime_title in data['name']:
                BOOK_ID = data['id']
                break
            
        response = requests.get(secrets['chapter_url']+"?count=300&sort=-created_at", headers=headers)
        list = response.json()

        for data in list['data']:
            if str(BOOK_ID) in str(data['book_id']):
                if data['name'] == season:
                    CHAPTER_ID = data['id']
                    break

        response = requests.get(secrets['chapter_url'] + str(CHAPTER_ID), headers=headers)
        length = len(response.json()['pages'])
        print("Expecting", length, "episodes")

        if season_length == len(response.json()['pages']):
            print("Season verified.")
        else:
            actual_eps = []
            miss = int(season_length) - int(length)
            print("Missing", miss, "episodes")
            for eps in response.json()['pages']:
                actual_eps.append(eps['name'])
            print("Missing:")
            for ep in episodes:
                if ep not in actual_eps:
                    print(ep)

    except (KeyError, JSONDecodeError) as error:
        print(error, "Couldn't verify. Check manually")

episodes = []
source_links = []

with open("links.json", 'r', encoding="utf8") as file:
    data = json.load(file)
    link_title = re.sub(r"['\"/;:&,?()<>.\\]", "", data['title']).replace(" ", "_")
    link_season = re.sub(r"['\"/;:&,?()<>.\\]", "", data['season']).replace(" ", "_")
    season_length = len(data['episodes'])
    for x, y in data['episodes'].items():
        episodes.append(x)
        source_links.append(y)

anime_title = data['title']
season = data['season']

verify_season(season_length)
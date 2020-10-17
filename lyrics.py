import configparser
import requests
from bs4 import BeautifulSoup
import re

def get_access_token():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['client_access_token']['token']
# test get_access_token()
# print(get_access_token())


token = get_access_token()


def search_music_artist(name):
    api_url = "https://api.genius.com/search?q={}".format(name)
    headers = {'authorization': token}
    r = requests.get(api_url, headers=headers)
    return r.json()
# test search_music_artis()
# print(search_music_artist("Drake"))


def get_artist_id(name):
    r = search_music_artist(name)
    id = r["response"]["hits"][0]["result"]["primary_artist"]["id"]
    return id
# test get_artist_id()
# print(get_artist_id("Drake"))


def get_top_songs(name):
    id = get_artist_id(name)
    # api_url = "https://api.genius.com/artists/{}/songs?sort=popularity&per_page=10".format(id)
    api_url = "https://api.genius.com/artists/{}/songs".format(id)
    headers = {"authorization": token}
    params = {
        "sort": "popularity",
        "per_page": 10
    }
    r = requests.get(api_url, headers=headers, params=params)
    return r.json()
# test get_top_songs()
# print(get_top_songs("Lenka", 20))


def get_lyrics_array(name):
    r = get_top_songs(name)
    songs = r["response"]["songs"]
    lyrics_array = []
    for song in songs:
        lyrics_array.append(song["url"])
    return lyrics_array
# test get_lyrics_array()
# print(get_lyrics_array("Drake", 15))

"""
def scrape_lyrics_text(name):
    links = get_lyrics_array(name)
    print(links)
    song_lyrics = []
    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        lyrics_div = soup.find(class_="lyrics")
        anchor_tags = lyrics_div.find_all('a')
        print(len(anchor_tags))
        current_lyrics = []
        # each anchor_tag corresponds to a line
        for anchor_tag in anchor_tags:
            print(anchor_tag.text)
            # get rid of lines like [Intro], [Chorus], [Verse 1], [Verse 2]
            if len(anchor_tag.text) > 0 and anchor_tag.text[0] != '[':
                # get rid of the new line symbol
                text = anchor_tag.text.replace("\n", " ")
                current_lyrics.append(text)
        #print(current_lyrics)
        song_lyrics.append(current_lyrics)
    # print(song_lyrics)
    return song_lyrics
# test scrape_lyrics_text()
# print(scrape_lyrics_text("drake", 12))
"""


def scrape_lyrics_text(name):
    links = get_lyrics_array(name)
    song_lyrics = []
    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        lyrics_div = soup.find(class_="lyrics")
        # all lyrics of a whole song can be found in <p>
        p_tags = lyrics_div.find_all('p')
        current_lyrics = []
        for p_tag in p_tags:
            # replace new line symbol with space
            text = p_tag.text.replace("\n", " NEWLINE ")
            # remove (, )
            text = text.replace("(", "")
            text = text.replace(")", "")
            # remove strings in brackets like [Intro], [Chorus], [Verse 1], [Verse 2]
            text = re.sub("\[.*?\]", "", text)
            # remove the space at the beginning of the text
            while text[0] == " ":
                text = text[1:]
            current_lyrics.append(text)
        song_lyrics.append(current_lyrics)
    # print(song_lyrics)
    return song_lyrics
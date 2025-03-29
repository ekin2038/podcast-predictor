import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
import re
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer

podcast_list=["Good Hang with Amy Poehler", 
              "The Mel Robbins Podcast",
              "The Joe Rogan Experience",
              "The Diary Of A CEO with Steven Bartlett",
              "Modern Wisdom",
              "Call Her Daddy",
              "Candace",
              "The Telepathy Tapes",
              "This Past Weekend w/Theo Von",
              "The MeidasTouch Podcast",
              "The Tucker Carlson Show",
              "Rotten Mango",
              "Shawn Ryan Show",
              "the zurkie show",
              "Khloé in Wonder Land",
              "House of Maher",
              "The Daily",
              "Good Guys",
              "THREE",
              "Crime Junkie",
              "IMO with Michelle Obama and Craig Robinson",
              "All-In with Chamath, Jason, Sacks & Adam Scott",
              "Up First from NPR",
              "Ryan Trahan",
              "Bad Friends",
              "Not Gonna Lie with Kylie Kelce",
              "The LOL Podcast",
              "ChainsFR On Spotify",
              "Ryth",
              "Matt and Shane's Secret Podcast",
              "Pretty Funny",
              "Huberman Lab",
              "The Charlie Kirk Show",
              "Crime, Conspiracy, Cults and Murder",
              "The Jefferson Fisher Podcast",
              "Aware and Aggravated",
              "The Martyr Made Podcast",
              "MrBallen Podcast Strange, Dark & Mysterious Stories",
              "Fly on the Wall with Dana Carvey and David Spade",
              "NPR News Now",
              "Common Sense with Dan Carlin",
              "The Ezra Klein Show",
              "On Purpose with Jay Shetty",
              "Morbid",
              "The Determined Society with Shawn French",
              "Smosh Reads Reddit Stories",
              "Smartless",
              "The Broski Report with Brittany Broski",
              "anything goes with emma chamberlain",
              "Late Nights with Nexpo",
              "The Megyn Kelly Show",
              "The Find Out Podcast",
              "This is Gavin Newsom",
              "CreepCast",
              "Rotten Mango Video",
              "Barely Famous",
              "Conan O'Brien Needs A Friend",
              "Armchair Expert with Dax Shepard",
              "The Rachel Maddow Show",
              "Pod Save America",
              "The Ben Shapiro Show",
              "The Journal.",
              "The Magnus Archives",
              "Killer Minds: Inside the Minds of Serial Killers & Murderers",
              "Therapuss with Jake Shane",
              "The White Lotus Official Podcast",
              "The Bryce Crawford Podcast",
              "The Weekly Show with Jon Stewart",
              "Duncanyounot",
              "2 Bears, 1 Cave with Tom Segura & Bert Kreischer",
              "Dateline NBC",
              "A Bit Fruity with Matt Bernstein",
              "PBD Podcast",
              "Giggly Squad",
              "Lemonade Stand",
              "Distractible",
              "Morning Brew Daily",
              "Stuff You Should Know",
              "Tony Mantor: Why Not Me the World",
              "Your Mom's House with Christina P.and Tom Segura",
              "Blink|Jake Haendel's Story",
              "Two Hot Takes",
              "The Brett Cooper Show",
              "Andrew Schulz's Flagrant with Akaash Singh",
              "Financial Audit",
              "The Commercial Break",
              "The Ultimate Human with Gary Brecka",
              "The Basement Yard",
              "The Bulwark Podcast",
              "The Oprah Podcast",
              "ann's audios ⋆.ೃ࿔*:･",
              "Nick DiGiovanni",
              "Ray William Johnson: True Story Podcast",
              "KILL TONY",
              "The Ramsey Show",
              "The Mindset Mentor",
              "Lex Fridman Podcast",
              "The Rest Is History",
              "Murder: True Stories"
              ]

SPOTIPY_CLIENT_ID = '87445bb1ca964d1fa56f5f31d06dd47e'
SPOTIPY_CLIENT_SECRET ='eddf084ff4c44cd2b897b029144963c9'

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def authenticate_spotify_and_fetch_data(search_query):
    # Authenticate with Spotify
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #search_query = "Good Hang with Amy Poehler"
    results = sp.search(q=search_query, type='show', limit=1)


    show = results['shows']['items'][0]
    print("Found podcast:", show['name'])
    print("Publisher:", show['publisher'])
    print("Show ID:", show['id'])


    episodes = []
    offset = 0

    while True:
        response = sp.show_episodes(show['id'], limit=50, offset=offset)
        items = response['items']
        
        if not items:
            break 

        for ep in items:
            if ep is None:
                continue
            episodes.append({
                'name': ep['name'],
                'release_date': ep['release_date'],
                'description': ep['description'],
                'duration_min': ep['duration_ms'] / 60000  # ms to minutes
            })

        offset += len(items)
    return episodes


def clean_description(desc):
    desc = desc.lower()

    # Remove punctuation and numbers
    desc = re.sub(r'[^a-z\s]', '', desc)

    # Tokenize into words
    words = desc.split()

    # Remove stop words
    words = [word for word in words if word not in stop_words]

    # Join back into a cleaned string
    return ' '.join(words)

collections={}

for i in range(len(podcast_list)):
    Episodes= authenticate_spotify_and_fetch_data(podcast_list[i])
    collections[podcast_list[i]]=Episodes


print("Retrieved "+str(len(collections))+" episodes")

#write the episodes in json file
with open('all.json', 'w', encoding='utf-8') as f:
    json.dump(collections, f, ensure_ascii=False, indent=2)


# Episodes=[]   
# #read the episodes again
# with open('Good_hang_with_amy_poehler_episodes.json', 'r', encoding='utf-8') as f:
#     Episodes = json.load(f)

# print("Read "+str(len(Episodes))+" episodes")

# for i in range(5):
#     ep=Episodes[i]
#     print(ep['name'])
#     print(ep['release_date'])
#     print(ep['description'])
#     print(ep['duration_min'])
#     print("\n")
    

#clean the description removing stop words and punctuation, numbers, special characters
# for ep in Episodes:
#     ep['cleaned_description']= clean_description(ep['description'])

# for i in range(5):
#     ep=Episodes[i]
#     print(ep['name'])
#     print(ep['release_date'])
#     print(ep['description'])
#     print(ep['cleaned_description'])
#     print(ep['duration_min'])
#     print("\n")

#convert the cleaned description into vectors using sentence transformer model(based on BERT)
#pre trained language model: all-MiniLM-L6-v2
# model = SentenceTransformer('all-MiniLM-L6-v2')
# for ep in Episodes:
#     ep['embedding'] = model.encode(ep['cleaned_description']).tolist()

# for i in range(5):
#     ep=Episodes[i]
#     print(ep['name'])
#     print(ep['release_date'])
#     print(ep['description'])
#     print(ep['cleaned_description'])
#     print(ep['duration_min'])
#     print(ep['embedding'])
#     print("\n")
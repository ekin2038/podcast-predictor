import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
import re
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer



SPOTIPY_CLIENT_ID = '87445bb1ca964d1fa56f5f31d06dd47e'
SPOTIPY_CLIENT_SECRET ='eddf084ff4c44cd2b897b029144963c9'

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def authenticate_spotify_and_fetch_data():
    # Authenticate with Spotify
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    search_query = "The Joe Rogan Experience"
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





# Episodes= authenticate_spotify_and_fetch_data()
# print("Retrieved "+str(len(Episodes))+" episodes")

# #write the episodes in json file
# with open('episodes.json', 'w', encoding='utf-8') as f:
#     json.dump(Episodes, f, ensure_ascii=False, indent=2)


Episodes=[]   
#read the episodes again
with open('episodes.json', 'r', encoding='utf-8') as f:
    Episodes = json.load(f)

print("Read "+str(len(Episodes))+" episodes")

# for i in range(5):
#     ep=Episodes[i]
#     print(ep['name'])
#     print(ep['release_date'])
#     print(ep['description'])
#     print(ep['duration_min'])
#     print("\n")
    

#clean the description removing stop words and punctuation, numbers, special characters
for ep in Episodes:
    ep['cleaned_description']= clean_description(ep['description'])

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
model = SentenceTransformer('all-MiniLM-L6-v2')
for ep in Episodes:
    ep['embedding'] = model.encode(ep['cleaned_description']).tolist()

# for i in range(5):
#     ep=Episodes[i]
#     print(ep['name'])
#     print(ep['release_date'])
#     print(ep['description'])
#     print(ep['cleaned_description'])
#     print(ep['duration_min'])
#     print(ep['embedding'])
#     print("\n")
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker
from collections import Counter
from datetime import datetime
from spotipy.exceptions import SpotifyException

SPOTIPY_CLIENT_ID = '87445bb1ca964d1fa56f5f31d06dd47e'
SPOTIPY_CLIENT_SECRET ='eddf084ff4c44cd2b897b029144963c9'
client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    )
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


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
              "Tony Mantor: Why Not Me the World"]


podcast_IDs=[]
all_info={}

def store_IDs():
    for podCast in podcast_list:
        results= sp.search(q=podCast,type='show', limit=1)
        show = results['shows']['items'][0]
        
        podcast_IDs.append(show['id'])


def safe_request(fn, *args, **kwargs):
    while True:
        try:
            return fn(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get("Retry-After", 5))

                # Convert to seconds if it looks like milliseconds
                if retry_after > 100:
                    retry_after = retry_after / 1000

                print(f"Rate limit hit on: {fn.__name__}")
                print(f"Retrying request to: {fn.__name__} after {retry_after:.2f} seconds...")
                time.sleep(retry_after)
            else:
                raise

            
            
def retrieve_episodes(show_name):
    episodes=[]
    offset=0
    while True:
        response = safe_request(sp.show_episodes, show_name, limit=50, offset=offset)
        #response = sp.show_episodes(show_name, limit=50, offset=offset)
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
    all_info[str]=episodes    

print(len(podcast_list))       
store_IDs()  
print(len(podcast_IDs))  
for i in range(len(podcast_IDs)):
    retrieve_episodes(podcast_IDs[i])
    time.sleep(30)

print(len(all_info))





# def authenticate_spotify_and_fetch_data():
#     client_credentials_manager = SpotifyClientCredentials(
#         client_id=SPOTIPY_CLIENT_ID,
#         client_secret=SPOTIPY_CLIENT_SECRET
#     )
#     sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
#     collected={}
#     search_terms = list("abcdefghijklmnopqrstuvwxyz")
    
#     market="US"
    
#     for term in tqdm(search_terms, desc="Searching"):
#         for offset in range(0, 1000, 50):
#             try:
#                 results = sp.search(q=term, type='show', limit=50, offset=offset, market=market)
#                 shows = results.get("shows", {}).get("items", [])
#             except Exception as e:
#                 print(f"Error: {e}")
#                 time.sleep(1)
#                 continue

#             if not shows:
#                 break

#             for show in shows:
#                 show_id = show["id"]
#                 if show_id not in collected:
#                     year_count = Counter()
#                     offset_ep = 0

#                     while True:
#                         try:
#                             eps_response = sp.show_episodes(show_id, limit=50, offset=offset_ep)
#                         except Exception as e:
#                             print(f"Error fetching episodes for {show['name']}: {e}")
#                             break

#                         items = eps_response.get("items", [])
#                         if not items:
#                             break

#                         for ep in items:
#                             if ep is None:
#                                 continue
#                             release_date = ep.get("release_date", "")
#                             if len(release_date) >= 4:
#                                 year = release_date[:4]
#                                 year_count[year] += 1

#                         offset_ep += len(items)
#                         if len(items) < 50:
#                             break
#                         time.sleep(0.1)  # optional: avoid rate limit

#                     collected[show_id] = {
#                         "id": show_id,
#                         "name": show["name"],
#                         "publisher": show["publisher"],
#                         "description": show["description"],
#                         "total_episodes": show["total_episodes"],
#                         "languages": show.get("languages", []),
#                         "spotify_url": show["external_urls"]["spotify"],
#                         "episodes_by_year": dict(year_count) 
#                     }

#                 if len(collected) >= 1000:
#                     break
#             if len(collected) >= 1000:
#                 break
#         if len(collected) >= 1000:
#             break
        
#     with open("top_1000_spotify_podcasts.json", "w", encoding="utf-8") as f:
#         json.dump(list(collected.values()), f, indent=2, ensure_ascii=False)
        
# client_credentials_manager = SpotifyClientCredentials(
#         client_id=SPOTIPY_CLIENT_ID,
#         client_secret=SPOTIPY_CLIENT_SECRET
#     )
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
# def collect_basic_podcasts():
#     collected = {}
#     search_terms = list("abcdefghijklmnopqrstuvwxyz")

#     for term in tqdm(search_terms):
#         for offset in range(0, 1000, 50):
#             if len(collected) >= 500:  # just grab 500 quick
#                 break
#             results = sp.search(q=term, type='show', limit=50, offset=offset, market='US')
#             for show in results['shows']['items']:
#                 show_id = show['id']
#                 if show_id not in collected:
#                     collected[show_id] = {
#                         "id": show_id,
#                         "name": show["name"],
#                         "publisher": show["publisher"],
#                         "description": show["description"],
#                         "total_episodes": show["total_episodes"]
#                     }
#         if len(collected) >= 500:
#             break

#     with open("basic_podcasts.json", "w") as f:
#         json.dump(list(collected.values()), f, indent=2)
    
    

# def plot_podcast_chunk(dataframe, chunk_number=0, chunk_size=100):
#     start = chunk_number * chunk_size
#     end = start + chunk_size
#     chunk = dataframe.iloc[start:end]

#     plt.figure(figsize=(12, chunk_size * 0.2))
#     sns.barplot(data=chunk, y="name", x="total_episodes", palette="crest")
#     plt.xlabel("Total Episodes")
#     plt.ylabel("Podcast Name")
#     plt.title(f"Podcasts {start+1}–{end} by Total Episodes")
#     plt.tight_layout()
#     plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
#     plt.show()

# #authenticate_spotify_and_fetch_data()
# #collect_basic_podcasts()

# with open("basic_podcasts.json") as f:
#     basic = json.load(f)

# # sort by total episodes, take top 50
# top = sorted(basic, key=lambda x: x["total_episodes"], reverse=True)[:20]

# enriched = []
# current_year = datetime.now().year
# target_years = {str(current_year), str(current_year - 1)}  # e.g., {'2024', '2023'}

# for show in top:
#     show_id = show["id"]
#     year_count = Counter()
#     offset = 0

#     while True:
#         try:
#             eps = sp.show_episodes(show_id, limit=50, offset=offset)
#         except Exception as e:
#             print(f"Error for {show['name']}: {e}")
#             break

#         items = eps.get("items", [])
#         if not items:
#             break

#         for ep in items:
#             if ep is None:
#                 continue
#             date = ep.get("release_date", "")
#             if len(date) >= 4:
#                 year = date[:4]
#                 if year in target_years:  # ✅ Only count recent 2 years
#                     year_count[year] += 1

#         offset += len(items)
#         if len(items) < 50:
#             break
#         time.sleep(0.2)

#     show["episodes_by_year"] = dict(year_count)
#     enriched.append(show)

# with open("top_podcasts_recent_2_years.json", "w", encoding="utf-8") as f:
#     json.dump(enriched, f, indent=2, ensure_ascii=False)

# Episodes=[]   
# #read the episodes again
# with open('top_1000_spotify_podcasts.json', 'r', encoding='utf-8') as f:
#     Episodes = json.load(f)    
# #print(len(Episodes))

# # df = pd.DataFrame(Episodes)
# # df_sorted = df.sort_values(by="total_episodes", ascending=False).reset_index(drop=True)  

# # for i in range(10):
# #     plot_podcast_chunk(df_sorted, chunk_number=i)
# episodes = [ep['total_episodes'] for ep in Episodes]
























































# plt.figure(figsize=(14, 6))
# plt.plot(range(1, len(episodes) + 1), sorted(episodes, reverse=True), marker='o', linewidth=1)
# plt.title("Total Episodes Across All 1000 Podcasts")
# plt.xlabel("Podcast Rank by Episode Count")
# plt.ylabel("Total Episodes")
# plt.grid(True)
# plt.tight_layout()
# plt.show()


#average for two years
# for ep in Episodes:
#     ep['average_episodes']= ep['total_episodes']/2

# episodes = [ep['average_episodes'] for ep in Episodes]

# plt.figure(figsize=(14, 6))
# plt.plot(range(1, len(episodes) + 1), sorted(episodes, reverse=True), marker='o', linewidth=1)
# plt.title("Average of all 1000 Podcasts for two years")
# plt.xlabel("Podcast Rank by average")
# plt.ylabel("Total Episodes")
# plt.grid(True)
# plt.tight_layout()
# plt.show()
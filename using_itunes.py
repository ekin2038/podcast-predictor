import requests
import feedparser
import json
from datetime import timezone
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#collected this ranked list from: https://podcastcharts.byspotify.com/
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

all_info={}

def search_podcast_on_apple(podcast_name):
    print("Searching for: "+podcast_name)
    params = {
        "term": podcast_name,
        "media": "podcast",
        "limit": 1
    }
    response = requests.get("https://itunes.apple.com/search", params=params)
    results = response.json().get("results", [])

    if not results:
        print(" Podcast not found.")
        return None

    podcast = results[0]
    if "feedUrl" not in podcast:
        return None
    return {
        "name": podcast["collectionName"],
        "publisher": podcast["artistName"],
        "rss_url": podcast["feedUrl"]
    }

def fetch_episodes_from_rss(rss_url):
    print(" Parsing RSS feed: "+rss_url)
    feed = feedparser.parse(rss_url)
    episodes = []

    for entry in feed.entries:
        episodes.append({
            "title": entry.get("title"),
            "published": entry.get("published"),
            "summary": entry.get("summary", ""),
            "duration": entry.get("itunes_duration", "unknown")
        })

    return episodes

def save_to_json(podcast_name, metadata, episodes):
    safe_name = podcast_name.replace(" ", "_").lower()
    filename = f"{safe_name}_episodes.json"

    data = {
        "podcast_name": metadata["name"],
        "publisher": metadata["publisher"],
        "rss_url": metadata["rss_url"],
        "episodes": episodes
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Saved to "+filename)

#uncomment these lines if you are running first time and don't have the all_podcasts_episodes.json file

# if __name__ == "__main__":
#     for i in range(len(podcast_list)):
#         metadata= search_podcast_on_apple(podcast_list[i])
#         if metadata:
#             time.sleep(1)  
#             episodes = fetch_episodes_from_rss(metadata["rss_url"])
#             print("Found "+str(len(episodes))+" episodes.")
#             all_info[podcast_list[i]]=episodes
#     with open("all_podcasts_episodes.json", "w", encoding="utf-8") as f:
#         json.dump(all_info, f, indent=2, ensure_ascii=False)


# Load data
with open("all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Use the order they appear in the JSON file
ordered_podcasts = list(data.keys())
episode_counts = [len(data[pod]) for pod in ordered_podcasts]
            
# Plot the podcasts
plt.figure(figsize=(14, 6))
plt.bar(ordered_podcasts, episode_counts)
plt.xticks(rotation=90, fontsize=8)
plt.ylabel("Number of Episodes")
plt.xlabel("Podcast (Ordered by Popularity)")
plt.title("Episode Count by Podcast Popularity Rank")
plt.tight_layout()
plt.show()

cutoff_date = datetime.now(timezone.utc) - timedelta(days=2 * 365)

def is_recent(ep):
    date_str = ep.get("release_date") or ep.get("published")
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        try:
            dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        except:
            return False
    return dt >= cutoff_date

avg_per_year = []
for name in ordered_podcasts:
    episodes = data[name]
    recent_eps = [ep for ep in episodes if is_recent(ep)]
    avg = len(recent_eps) / 2 
    avg_per_year.append(avg)
            
plt.figure(figsize=(14, 6))
plt.bar(ordered_podcasts, avg_per_year)
plt.xticks(rotation=90, fontsize=8)
plt.ylabel("Average Episodes per Year (Last 2 Years)")
plt.xlabel("Podcast (in Popularity Order)")
plt.title("Average of the podcasts for Last 2 Years based on the number of episodes for each podcast)")
plt.tight_layout()
plt.show()

    

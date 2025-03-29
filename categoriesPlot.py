import requests
import time
import json
import matplotlib.pyplot as plt
from collections import defaultdict

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


categories = defaultdict(list)

def fetch_itunes_category(podcast_name):
    print(" Searching: "+podcast_name)
    params = {
        "term": podcast_name,
        "media": "podcast",
        "limit": 1
    }
    try:
        response = requests.get("https://itunes.apple.com/search", params=params)
        results = response.json().get("results", [])
        if not results:
            print(" No result found for: "+podcast_name)
            return "Unknown"
        return results[0].get("primaryGenreName", "Unknown")
    except Exception as e:
        print(" Error fetching category for "+podcast_name+e)
        return "Unknown"
    
for name in podcast_list:
    temp= fetch_itunes_category(name)
    categories[temp].append(name)
    #time.sleep(0.5)
    
    
category_counts = {cat: len(pods) for cat, pods in categories.items()}


sorted_counts = dict(sorted(category_counts.items(), key=lambda x: x[1], reverse=True))

plt.figure(figsize=(14, 6))
plt.bar(sorted_counts.keys(), sorted_counts.values(), color='mediumslateblue')
plt.xticks(rotation=90, fontsize=8)
plt.ylabel("Number of Podcasts")
plt.title("Number of Podcasts per Category")
plt.tight_layout()
plt.show()
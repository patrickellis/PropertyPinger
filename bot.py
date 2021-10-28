# bot.py
import os
import requests
import json
import discord
from dotenv import load_dotenv
from RightmoveData import RightmoveData
import pandas as pd
from IPython.display import display
import time
from datetime import datetime, timedelta

# Define constants from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')
RIGHTMOVE_FILE = os.getenv('RIGHTMOVE_FILE')
ZOOPLA_FILE = os.getenv('ZOOPLA_FILE')
NUM_ITERATIONS = 300
SEARCH_INTERVAL = 300
POST_DELAY = 30
LASTCALL = datetime.today() - timedelta(hours=0, minutes=60)
# last discord post time stored to avoid having requests rejected

#search queries to scrape on RIGHTMOVE
SCRAPES = [
    "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E85314&maxBedrooms=3&minBedrooms=3&maxPrice=2750&minPrice=1750&radius=0.5&propertyTypes=&maxDaysSinceAdded=1&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=",
    "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E85314&maxBedrooms=3&minBedrooms=3&maxPrice=2750&minPrice=1750&radius=0.5&propertyTypes=&maxDaysSinceAdded=1&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=",
    "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E85244&maxBedrooms=3&minBedrooms=3&maxPrice=2750&minPrice=1750&radius=0.5&propertyTypes=&maxDaysSinceAdded=1&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=",
    "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87492&maxBedrooms=3&minBedrooms=3&maxPrice=2750&minPrice=1750&radius=0.5&propertyTypes=&maxDaysSinceAdded=1&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=",
    "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E85329&maxBedrooms=4&minBedrooms=3&maxPrice=3000&minPrice=1750&radius=0.5&propertyTypes=&maxDaysSinceAdded=3&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="
]


def write_to_file(file, items):
    """Write scraped links to a file so that they will not be pinked even
    between multiple runs of the program.
    Args:
        file (str) : file to be written to
        items (list(str)) : links to be written.
    """
    if not items:
        return
    with open(file, 'a+') as f:
        for item in items:
            f.write("%s\n" % item)

def scrape(url):
    rm = RightmoveData(url)
    return rm.get_results['url'].tolist()

def make_post(url):
    """Makes HTTP post request to discord channel. Posts given URL.
    Args:
        url (str) : url to post
    """
    global LASTCALL
    currentTime = datetime.today()
    if((currentTime - LASTCALL).total_seconds() < POST_DELAY):
        time.sleep(POST_DELAY-(currentTime - LASTCALL).total_seconds())
    LASTCALL = datetime.today()
    baseURL = "https://discordapp.com/api/channels/{}/messages".format(CHANNEL)
    headers = { "Authorization":"Bot {}".format(TOKEN),
            "User-Agent":"myBotThing (http://some.url, v0.1)",
            "Content-Type":"application/json", }
    message = url
    POSTedJSON =  json.dumps ( {"content":message} )
    r = requests.post(baseURL, headers = headers, data = POSTedJSON)


def rightmove_scrape(properties):
    """Scrapes rightmove based on the queries in SCRAPES.
    Args:
        properties (set(str)) : set of links that have been posted already.
    """
    newlinks = []
    for target in SCRAPES:
        results = scrape(target)
        for result in results:
            if result not in properties:
                properties.add(result)
                newlinks.append(result)
                make_post(result)
    write_to_file(RIGHTMOVE_FILE,newlinks)

if __name__ == '__main__':
    print("starting program...")
    links = None
    with open(RIGHTMOVE_FILE) as file:
        lines = file.readlines()
        links = [line.rstrip() for line in lines]
    properties = set(links)

    # main driver
    for iteration in range(NUM_ITERATIONS):
        rightmove_scrape(properties)
        time.sleep(SEARCH_INTERVAL)

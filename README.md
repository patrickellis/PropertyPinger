# PropertyPinger
A web scraper bot to search for new web listings that match a set of filters and sends pings to a given discord channel

## How to use
| Unix/macOS  |   Windows   |
| ----------- | ----------- |
| python -m pip install -r requirements.txt | py -m pip install -r requirements.txt      |
* edit the SCRAPES constant variable in the bot.py file
* to generate a link that is appropriate for your search, go to rightmove.co.uk and enter a location and select a set of filters, press search and copy this URL into **SCRAPES**
* create yourself a bot on the [discord developer portal](https://discord.com/developers/docs/intro)
* run the bot.py file, or host it on a VM for 24/7 script operation
*
## How to find your Discord Channel Token
* enable developer mode on your discord app (Settings -> Advanced -> Developer Mode)
* right click on the channel you want to send pings to -> Copy ID

## How to create a discord bot 
Follow the instructions [here](https://realpython.com/how-to-make-a-discord-bot-python/) to create a bot and add it to a discord server. (10 minutes est.) 

## Config 
There are a set of Constants that you can configure to change the behaviour of the bot, here are the most important ones:
* POST_DELAY (Default 30) - the time (in seconds) between posts to discord, I've set it to 30 to avoid the bot being timed out but you can experiment with making it lower
* SEARCH_INTERVAL (Default 300) - the time (in seconds) between scrapes of the rightmove links in **SCRAPES**. Searching every 5 minutes has worked well for me. 


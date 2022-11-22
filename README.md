# Hangman game with discord bot integration

Made for [czech university information technology seminar](https://ksi.fi.muni.cz/ulohy/514)

## How to play

1. Put `app.py` and `words.txt` files in the same directory
1. Get the latest release of Python [here](https://www.python.org/downloads/).
1. Install discord.py and python-dotenv in console using:
   - Linux/macOS: `python3 -m pip install -U discord.py` and `python3 -m pip install -U python-dotenv`
   - Windows: `py -3 -m pip install -U discord.py` and `py -3 -m pip install -U python-dotenv`
1. [Create a Discord bot and get its token](https://www.writebots.com/discord-bot-token/)
1. Create an `.env` (no name) file in the same direcotry as your `app.py` file with:

```
TOKEN=<your discord bot token>
```

4. Run `discord_bot.py`

You can change the words in `words.txt` file to your liking

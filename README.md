# Cloaky Proteus
Cloaky Proteus is a discord bot who's sole purpose is to perform a character lookup for Eve Online. It's written in python using the [discord.py rewrite](https://github.com/Rapptz/discord.py) and [esipy](https://github.com/Kyria/EsiPy) libraries. 

# Requirements
* Windows
* [Python 3.7](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html)

## Installation
1. Download a copy of Cloaky Proteus from the [releases page](https://github.com/Mav986/cloakyproteus/releases) and extract the files into a location of your choice. 
2. Open a command prompt and navigate to the Discord directory within the project folder.
3. Run the following command; it may take a few minutes:
   
        python install.py

## Configuration
Once environment setup completes, you will need to set up a couple config files
   1. Log into the [Discord Developer Portal](https://discordapp.com/developers/applications/)
   2. Create a new Application with whatever name you like (this is not the name that appears in Discord)
   3. Navigate to the "Bot" section in the left menu
   4. Add Bot ("Yes, do it")
   5. Call the bot whatever you want your bot to be named in Discord
   6. Turn "Public bot" slider to off
   7. Copy token
   8. Configure the bot to use the Discord token
      1. In Windows, navigate to the Discord directory within the bot's project
      2.  Rename "_config.dist.py" to "_config.py" and open it in your choice of text editor
      3.  Replace "DISCORD TOKEN HERE" with the copied token
      4.  Save and close the file
   9.  Configure the bot with a way for CCP to contact you should the bot do something bad
       1.  In Windows, navigate to the Esi directory within the bot's project
       2.  Rename "_config.dist.py" to "_config.py" and open it in your choice of text editor
       3.  Replace "USER-AGENT-HERE" with your preferred method of being contacted 
           * `"Email: me@example.com"`
           * `"Discord: me#1234"`
           * `"EVE Online: MyCharacterName"`
       4.  Save and close the file

## Run
* Run the following command in the project folder using command prompt

        python start.py
# Utility Necrobot - Command tracking

### Warning:
```
I wrote this bot in 2021, it was one of the first discord bots I created, so the code you will
find in this repository is very bad, it violates most clean code practices and it's hard to navigate.
All functions are in a few files, with little comments, and a lot of duplicate code.

Feel free to use this code as you wish.
``` 

## What's this?
A discord bot for tracking epic rpg commands, very detailed, written in python/discord.py.

## How to set up?

1. Clone this repository using `git clone [url]`, where url is the link to the github repository.
2. Install python (3.11 or higer recommended)
3. Create a venv: navigate to the folder where you cloned the repository, open a terminal (cmd) and run these commands:
    - `python -m venv venv`
    - `venv\Scripts\activate.bat`
   - After the commands above you should see a `(venv)` in front of the path in the terminal.
   
4. Install the requirements using `pip install -r requirements.txt` 
5. Open the settings.py file and fill in the required fields.
    - `BOT_TOKEN` - Your bot's token. To get it, follow this tutorial: https://discordpy.readthedocs.io/en/stable/discord.html

6. Run the bot using `python main.py`

import discord
from discord.ext import commands
import os
import json

#reads token.txt, helps ensure we don't edit the token for this bot on accident in this file
TOKEN = open("disc_token.txt", "r").read()

#loads json file for server prefix, else default
def get_prefix(client, message):
    #default invoke command when prefix is not called within the server
    if not message.guild:
        #allows user to mention bot to invoke command
        return commands.when_mentioned_or("!")(client, message)

    #read json file as a dictionary.
    #json file contains guild ID as the key, and prefix as the value
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    #default invoke when guild has not set custom prefix
    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("!")(client, message)

    #grab the prefix per server based on guild id
    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(client, message)

#commands.Bot is the discord.Client object,
#extended with the functionality of the commands extension
#define default command prefix as !
client = commands.Bot(command_prefix=get_prefix)

#load every cogs file upon startup, owner.py has control
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

#bot status
@client.event
async def on_ready():
    print(f'\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}')
    print("-" * 42)
    await client.change_presence(activity=discord.Game("askhelp"))
    print(f'Successfully logged in and booted...!')

#general error handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

#run the bot, last line of code
client.run(TOKEN)
import discord
from discord.ext import commands
import os

#reads token.txt, helps ensure we don't edit the token for this bot on accident in this file
TOKEN = open("rank_token.txt", "r").read()

client = commands.Bot(command_prefix="!")

#load every cogs file upon startup, owner.py has control
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

#bot status
@client.event
async def on_ready():
    print(f'\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}')
    print("-" * 42)
    await client.change_presence(activity=discord.Game("with fire"))
    print(f'Successfully logged in and booted...!')

#general error handler
#@client.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.CommandNotFound):
#        pass

#run the bot, last line of code
client.run(TOKEN)





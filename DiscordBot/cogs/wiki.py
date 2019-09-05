import discord
from discord.ext import commands

import random
import asyncio

class Wiki(commands.Cog):

    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Wiki(client))
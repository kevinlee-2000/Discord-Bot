import discord
from discord.ext import commands

from bs4 import BeautifulSoup
import requests

import random

class Quote(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def quote(self, ctx):

        quote_list = []

        #the website only has 10 pages, 0-9 = 1-10
        for i in range(9):
            website = f"http://quotes.toscrape.com/page/{i+1}/"
            source = requests.get(website).text
            #use beautiful soup scraper, passing in source as the website to be scraped, and lxml as the parser
            soup = BeautifulSoup(source, 'lxml')

            for quote in soup.find_all(class_='quote'):

                quoteActual = quote.find(class_="text").text
                author = quote.find(itemprop='author').text

                quote_store = f"{quoteActual}-{author}"
                quote_list.append(quote_store)

        len_list = len(quote_list)
        i = random.randint(0, len_list)
        random_quote = quote_list[i]

        await ctx.send(random_quote)

def setup(client):
    client.add_cog(Quote(client))
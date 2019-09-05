import discord
from discord.ext import commands

import random
import asyncio

class RNG(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def dinosaur(self, ctx):
        await ctx.send(None, file=discord.File('cogs/anime_dino.gif'))

    # create a 8ball/fortune command
    # https://en.wikipedia.org/wiki/Magic_8-Ball
    # Note: 10 yes, 5 neutral, 5 no
    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.',
                     "It is decidely so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        questionLowerCase = str(question).lower()
        gaySynonyms = ["gay", "sus", "homo"]
        if any(gayWord in questionLowerCase for gayWord in gaySynonyms):
            responsesPos = responses[0:10]
            await ctx.send(f"{random.choice(responsesPos)}")
        else:
            await ctx.send(f"{random.choice(responses)}")

    # define flipping a coin
    # uses markdown from link
    # https://gist.github.com/Almeeida/41a664d8d5f3a8855591c2f1e0e07b19
    @commands.command()
    async def flip(self, ctx):

        HEAD_TIMER = 3.9
        TAIL_TIMER = 4.5

        # use random to determine half chance
        halfChance = random.randint(0, 1)  # numbers 0 or 1

        # assign timers based on number, to match gif speed
        if halfChance == 0:
            deleteTimer = HEAD_TIMER
        else:
            deleteTimer = TAIL_TIMER

        # send the gif on a timer
        await ctx.send(None, file=discord.File('cogs/coinflip/coin-flip.gif'), delete_after=deleteTimer)

        # send heads/tails
        if halfChance == 0:
            await asyncio.sleep(HEAD_TIMER)
            await ctx.send(None, file=discord.File('cogs/coinflip/head.JPG'))
            await ctx.send("```css\nHEADS```")
        else:
            await asyncio.sleep(TAIL_TIMER)
            await ctx.send(None, file=discord.File('cogs/coinflip/tails.JPG'))
            await ctx.send("```prolog\nTAILS```")


    #define random animals command
    @commands.command(aliases=["spirit"])
    async def spiritanimal(self,ctx):
        animalEmojis = [":dog:",
                        ":cat:",
                        ":mouse:",
                        ":hamster:",
                        ":rabbit:",
                        ":bear:",
                        ":panda_face:",
                        ":koala:",
                        ":tiger:",
                        ":lion:",
                        ":cow:",
                        ":pig:",
                        ":frog:",
                        ":octopus:",
                        ":monkey_face:",
                        ":penguin:",
                        ":bird:",
                        ":hatching_chick:",
                        ":wolf:",
                        ":horse:",
                        ":unicorn:",
                        ":snake:",
                        ":turtle:",
                        ":tropical_fish:",
                        ":dolphin:",
                        ":whale:",
                        ":elephant:",
                        ":goat:",
                        ":chipmunk:",
                        ":dragon_face:"]
        animalRandom = random.choice(animalEmojis)
        if animalRandom == ":dragon_face:":
            await ctx.send(f"Your spirit animal is the ***mighty*** {animalRandom}")
        elif animalRandom == ":unicorn:":
            await ctx.send(f"Your spirit animal is the _*magical*_ {animalRandom}")
        elif animalRandom == ":goat:":
            await ctx.send(f"Your spirit animal is - THE G.O.A.T. {animalRandom}")
        else:
            await ctx.send(f"Your spirit animal is a {animalRandom}")

    #troll frog
    @commands.command()
    async def frogo(self,ctx):
        await ctx.send(None, file=discord.File('cogs/frog.png'))

def setup(client):
    client.add_cog(RNG(client))
import discord
from discord.ext import commands
import requests
import json
import regex

RIOT_API_KEY = open("riot_api_key.txt", "r").read()
RIOT_API_KEY = str(RIOT_API_KEY)

class League(commands.Cog):

    def __init__(self, client):
        self.client = client


    #specific to grabbing the json response from league API
    def get_summoner_data(region, summoner):

        global RIOT_API_KEY

        #URL for riot games request
        SUMMONER_URL = "https://"+str(region)+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"\
                         +str(summoner)+"?api_key="+str(RIOT_API_KEY)

        #store the response we obtain from riot,
        response = requests.get(SUMMONER_URL)

        #return it in a json format
        return json.loads(response.text)

    #function follows similar format to the get_summoner_data
    def get_ranked_data(region, ID):

        global RIOT_API_KEY

        #url for summoner ranked data
        RANKED_DATA_URL = "https://"+str(region)+".api.riotgames.com/lol/league/v4/entries/by-summoner/"+\
                          str(ID)+"?api_key="+str(RIOT_API_KEY)

        #grabs ranked data
        response = requests.get(RANKED_DATA_URL)

        #api call gives [] which needs to be removed for the json to load as type 'dict' instead of type 'list'
        response_remove_bracket = str(response.text).replace('[','').replace(']','')

        if(len(response_remove_bracket) == 0):
            return "Unranked"
        else:
            return json.loads(response_remove_bracket)

    #check valid summoner id characters
    def valid_summoner_name(summoner):

        #regex given from league API allows only:
        #visible Unicode letter characters, digits (0-9), spaces, underscores, and periods
        x = regex.search(r"^[0-9_\. \p{L}]+$", str(summoner))
        if x is None:
            return False
        else:
            return True

    @commands.command()
    async def nalol(self, ctx, *, summoner):

        #check proper summoner name
        check_valid_summoner = League.valid_summoner_name(summoner)

        if check_valid_summoner == False:
            await ctx.send("Please enter a valid summoner ID")
        else:
            #specify the region
            region = "NA1"

            #grab id
            summonerJSON = League.get_summoner_data(str(region),str(summoner))
            summID = str(summonerJSON['id'])

            #check ranked stats
            rankedJSON = League.get_ranked_data(str(region), str(summID))
            if rankedJSON == "Unranked":
                embed = discord.Embed(color=0xf1c40f)
                embed.set_author(name=summoner)
                embed.add_field(name="Unranked", value="No data here")
                await ctx.send(embed=embed)
            else:
                summonerName = str(rankedJSON['summonerName'])
                tier = str(rankedJSON['tier'])
                rank = str(rankedJSON['rank'])
                wins = str(rankedJSON['wins'])
                losses = str(rankedJSON['losses'])
                leaguePoints = str(rankedJSON['leaguePoints'])
                embed = discord.Embed(color=0xf1c40f)
                embed.set_author(name=summonerName)
                embed.add_field(name=tier+" "+rank, value="League Points(LP): "+leaguePoints+"\nWin/Loss: "+wins+"-"+losses)
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(League(client))
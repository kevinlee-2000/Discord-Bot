import discord
from discord.ext import commands

from tempfile import NamedTemporaryFile
import shutil
import csv

import ast

class Member(commands.Cog):

    def __init__(self,client):
        self.client = client

    # handles when a new member joins a channel
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"{member.mention} has joined the server!!! "
                               f"I am AskBot:robot:. "
                               f"Ask me anything you want :cowboy:")

    # handles when a member
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"{member.mention} has left the server :poop:")

    #define a check per server id and if they have started a vote process yet
    def check_vote(self,ctx):
        with open(r"cogs/poll.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file)

            #skips header
            next(csv_reader)

            #loop through every line of the csv file
            for line in csv_reader:
                #csv file format, 0th element is the serverID
                serverID = int((line[0].strip()))
                startedPoll = line[1].strip()

                #check if the current server is in the csv file
                if ctx.guild.id == serverID:
                    #grab the boolean flag value
                    if startedPoll == "true":
                        return True
                    elif startedPoll == "false":
                        return False

            #server not in the history list
            #add a new server to the csv file and give it default values defined below
            with open(r"cogs/poll.csv", "a", newline = '') as f:
                entry = [str(ctx.guild.id), "false", "/empty","[]", "[]", "[]"]
                writer = csv.writer(f)
                writer.writerow(entry)
                return False

    #start a poll
    @commands.command()
    async def poll(self, ctx, *, question_and_votes):

        #check if poll is still active
        checkBool = Member.check_vote(self,ctx)

        if checkBool == True:
            await ctx.send("Poll is still active, please end it to start a new one")
        #means poll is not active and thus create one or update the values accordingly
        else:
            if "?" not in question_and_votes and ";" not in question_and_votes:
                await ctx.send("Please follow the format: Use '?' to denote the question "
                               "and ';' before each answer choice:\n Example: !poll is this bot cool?;yes;no;maybe")
            elif "?" not in question_and_votes:
                await ctx.send("Add a '?' to denote the question")
            elif ";" not in question_and_votes:
                await ctx.send("Add semicolons to denote the answer choices")
            else:
                #parse question_and_votes
                # wrap to a string and make variable easier to use
                parsedInfo = str(question_and_votes)
                # declare list that we will return in this string after everything is parsed
                list_content = []
                list_vote_counter = []
                list_voters_data = []

                # handles the question
                indexQuestion = parsedInfo.find("?")
                question = parsedInfo[0:indexQuestion + 1]
                longString = f"__{question}__" + "\n\n"

                # handles the choices
                count_semicolons = parsedInfo.count(";")
                # first semicolon after the index
                semicolon_index = parsedInfo.find(";")

                # begin loop parsing the answer choices
                for i in range(count_semicolons):
                    if i == count_semicolons-1:
                        answer = parsedInfo[semicolon_index+1: len(parsedInfo)]
                        list_content.append(answer)
                        list_vote_counter.append(str(0))
                        longString = longString + f"**{i+1}**" + ". " + answer
                    else:
                        # find the end index to substring from
                        nextSemi = parsedInfo.find(";", semicolon_index + 1, len(parsedInfo))
                        answer = parsedInfo[semicolon_index + 1: nextSemi]
                        list_content.append(answer)
                        list_vote_counter.append(str(0))
                        semicolon_index = nextSemi
                        longString = longString + f"**{i+1}**" + ". " + answer + "\n"

                temp_file = NamedTemporaryFile(delete=False,mode='w',newline='')

                #open the csv file and update information
                with open(r"cogs/poll.csv", 'r+',newline='') as csv_file, temp_file:
                    reader = csv.reader(csv_file)
                    writer = csv.writer(temp_file)

                    #header append to the temp file
                    header = next(reader)
                    writer.writerow(header)

                    for line in reader:
                        serverID = int((line[0].strip()))
                        if ctx.guild.id == serverID:
                            #create a new line that overwrites the old line
                            line = [str(ctx.guild.id), "true", str(question),list_content,list_vote_counter,
                                    str(list_voters_data)]
                        writer.writerow(line)

                #moves the file
                shutil.move(temp_file.name, r"cogs/poll.csv")

                # begin display process
                # note display_name refers to unique username of server
                display = f"{ctx.author.display_name} has started a poll"

                # change the display to include dashes lines on bottom
                lenDisplay = len(display)
                numOfDashes = "-" * (lenDisplay + 8)
                display = display + "\n" + numOfDashes

                # 0xf1c40f = gold
                embed = discord.Embed(color=0xf1c40f, timestamp=ctx.message.created_at)
                embed.set_author(name=display, icon_url=ctx.author.avatar_url)
                embed.add_field(name=longString, value="_Enter corresponding number to vote_")
                await ctx.send(embed=embed)

    #poll error handler
    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the format: Use '?' to denote the question "
                           "and ';' to indicate answer choices")

    @commands.command(aliases=["votestats"])
    async def pollstats(self, ctx):

        # check if poll is still active
        checkBool = Member.check_vote(self, ctx)
        if checkBool == True:
            longString = ""
            sumOfVotes = 0
            #parse the dictionary
            #recall format is key = number, "string";counter value
            with open(r"cogs/poll.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)
                counter = 0
                for line in reader:
                    serverID = int((line[0].strip()))
                    if ctx.guild.id == serverID:
                        question = str(line[2])
                        choices = str(line[3])
                        votes = str(line[4])
                        #convert type string to an actual list object
                        choices = choices.strip('][').split(', ')
                        votes = votes.strip('][').split(', ')

                        longString = f"__{question}__" +"\n\n"

                        number = 0
                        sumOfVotes = 0
                        for choice in choices:
                            choice = choice.strip("\'")
                            votes[number] = votes[number].strip('\'')
                            votes[number] = votes[number].strip()
                            votes[number] = int(votes[number])
                            #this is the main question
                            if votes[number] == 1:
                                longString = longString + f"**{number + 1}**" + ". " + f"{choice} " + \
                                             f"has __{votes[number]}__ vote" + "\n"
                                sumOfVotes += int(votes[number])
                            else:
                                longString = longString + f"**{number+1}**" + ". " + f"{choice} "+\
                                             f"has __{votes[number]}__ votes"+"\n"
                                sumOfVotes += int(votes[number])
                            number += 1

            display = "Current Poll Stats"
            lenDisplay = len(display)
            numOfDashes = "-" * (lenDisplay + 8)
            display = display + "\n" + numOfDashes
            #0x2ecc71 is the green color in Discord
            embed = discord.Embed(color=0x2ecc71,timestamp=ctx.message.created_at)
            embed.set_author(name=display, icon_url=ctx.author.avatar_url)
            embed.add_field(name=longString, value=f"_Total vote count: {sumOfVotes}_")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Start a poll to see the stats")

    #helper method for member registry
    def check_member_registry(self,ctx):
        with open(r"cogs/poll.csv", 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for line in reader:
                serverID = int((line[0].strip()))
                if ctx.guild.id == serverID:
                    member_registry = str(line[5])
                    # convert type string to an actual list object
                    member_registry = member_registry.strip('][').split(', ')
                    try:
                        for member in member_registry:
                            semiIndex = member.find(";")
                            member_id = member[0:semiIndex]
                            member_id = member_id.strip('\'')
                            member_id = member_id.strip()
                            if str(ctx.author.id) == member_id:
                                return True
                        return False
                    #note except block occurswhen there are is nothing in the member registry list
                    except:
                        return False

    #check that a number is valid
    #we are going to define our codes
    def validNumber(self,ctx, singleNumber):
        try:
            singleNumber = int(singleNumber)
        except ValueError:
            return 0
        if int(singleNumber) <= 0:
            return 1
        with open(r"cogs/poll.csv", 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for line in reader:
                serverID = int((line[0].strip()))
                if ctx.guild.id == serverID:
                    answer_choices = str(line[3])
                    # convert type string to an actual list object
                    answer_choices = answer_choices.strip('][').split(', ')
                    len_choices = len(answer_choices)
                    if singleNumber > len_choices:
                        return 2

    @commands.command(aliases=["v"])
    async def vote(self,ctx, singleNumber):

        checkBool = Member.check_vote(self, ctx)
        if checkBool == True:
            #use helper method for checks
            exitNum = Member.validNumber(self,ctx,singleNumber)
            if exitNum == 0:
                await ctx.send("Please enter a valid number")
            elif exitNum == 1:
                await ctx.send("Number entered isn't a voting option")
            elif exitNum == 2:
                await ctx.send("Number entered is beyond voting range")
            else:
                # reset the csv for the server back to a false
                temp_file = NamedTemporaryFile(delete=False, mode='w', newline='')

                # open the csv file and update the voter registry (track who voted and what option)
                with open(r"cogs/poll.csv", 'r+', newline='') as csv_file, temp_file:
                    reader = csv.reader(csv_file)
                    writer = csv.writer(temp_file)

                    # header append to the temp file
                    header = next(reader)
                    writer.writerow(header)
                    singleNumber = int(singleNumber)
                    for line in reader:
                        serverID = int((line[0].strip()))
                        if ctx.guild.id == serverID:

                            #have to grab the member_registry list in both conditions
                            member_registry = str(line[5])
                            # convert type string to an actual list object
                            member_registry = ast.literal_eval(member_registry)
                            member_registry = [n.strip() for n in member_registry]

                            check_registered = Member.check_member_registry(self, ctx)

                            # means voter intends to change vote
                            if check_registered == True:

                                idx_track = 0

                                for member in member_registry:

                                    #cleanly parse data
                                    semiIndex = member.find(";")
                                    member_id = member[0:semiIndex]
                                    member_id = member_id.strip('\'')
                                    member_id = member_id.strip()
                                    vote_stored = member[semiIndex+1:len(member)]
                                    vote_stored = vote_stored.strip('\'')
                                    vote_stored = vote_stored.strip()

                                    if str(ctx.author.id) == member_id:
                                        if(str(singleNumber) == vote_stored):
                                            await ctx.message.delete()
                                            await ctx.send(f"{ctx.author.display_name} already voted for this",
                                                           delete_after=2.5)
                                        else:
                                            #have to change vote counts up and down
                                            vote_count = str(line[4])
                                            vote_count = ast.literal_eval(vote_count)
                                            vote_count = [n.strip() for n in vote_count]
                                            vote_stored = int(vote_stored)
                                            subtract = (int(vote_count[vote_stored - 1]))
                                            subtract -= 1
                                            vote_count[vote_stored-1] = str(subtract)
                                            addition = int((vote_count[singleNumber - 1]))
                                            addition += 1
                                            vote_count[singleNumber-1] = str(addition)

                                            new_data = str(member_id) + ";" + str(singleNumber)
                                            #update the value now
                                            member_registry[idx_track] = new_data

                                            #update the file too
                                            line = [str(ctx.guild.id), "true", str(line[2]), str(line[3]),
                                                    vote_count, member_registry]
                                            await ctx.message.delete()
                                            await ctx.send(f"{ctx.author.display_name} has changed their vote",
                                                           delete_after=2.5)

                                    idx_track += 1

                            #means the user has never voted before
                            else:
                                member_data = str(ctx.author.id) + ";" + str(singleNumber)

                                #determines initial append or not
                                member_registry.append(member_data)

                                #increment the voting value
                                vote_count = str(line[4])
                                vote_count = ast.literal_eval(vote_count)
                                vote_count = [n.strip() for n in vote_count]
                                addition = int((vote_count[singleNumber - 1]))
                                addition += 1
                                vote_count[singleNumber - 1] = str(addition)
                                line = [str(ctx.guild.id), "true", str(line[2]), str(line[3]), vote_count,
                                        member_registry]
                                await ctx.message.delete()
                                await ctx.send(f"{ctx.author.display_name} has cast their vote",
                                               delete_after=2.5)
                        writer.writerow(line)

                # moves the file
                shutil.move(temp_file.name, r"cogs/poll.csv")
        else:
            await ctx.send("Start a poll to vote")

    @commands.command()
    async def pollend(self, ctx):

        checkBool = Member.check_vote(self, ctx)

        if checkBool == True:
            longString = ""
            sumOfVotes = 0
            # parse the dictionary
            # recall format is key = number, "string";counter value
            with open(r"cogs/poll.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)
                counter = 0
                for line in reader:
                    serverID = int((line[0].strip()))
                    if ctx.guild.id == serverID:
                        question = str(line[2])
                        choices = str(line[3])
                        votes = str(line[4])
                        # convert type string to an actual list object
                        choices = choices.strip('][').split(', ')
                        votes = votes.strip('][').split(', ')

                        #question to display
                        longString = f"__{question}__" + "\n\n"

                        number = 0
                        for choice in choices:
                            choice = choice.strip("\'")
                            votes[number] = votes[number].strip('\'')
                            votes[number] = votes[number].strip()
                            votes[number] = int(votes[number])
                            # this is the main question
                            longString = longString + f"**{number + 1}**" + ". " + f"{choice} " + \
                                         f"has __{votes[number]}__ votes" + "\n"
                            sumOfVotes += int(votes[number])
                            number += 1

            display = "Poll has ended"
            lenDisplay = len(display)
            numOfDashes = "-" * (lenDisplay + 8)
            display = display + "\n" + numOfDashes
            # 0xe74c3c = red
            # embed process, remove the message after certain time
            embed = discord.Embed(color=0xe74c3c, timestamp=ctx.message.created_at)
            embed.set_author(name=display, icon_url=ctx.author.avatar_url)
            embed.add_field(name=longString, value=f"_Total vote count: {sumOfVotes}_")
            await ctx.send(embed=embed)

            #reset the csv for the server back to a false
            temp_file = NamedTemporaryFile(delete=False, mode='w', newline='')

            # open the csv file and update information
            with open(r"cogs/poll.csv", 'r+', newline='') as csv_file, temp_file:
                reader = csv.reader(csv_file)
                writer = csv.writer(temp_file)

                # header append to the temp file
                header = next(reader)
                writer.writerow(header)

                for line in reader:
                    serverID = int((line[0].strip()))
                    if ctx.guild.id == serverID:
                        # create a new line that overwrites the old line
                        line = [str(ctx.guild.id), "false", "/empty", "[]", "[]", "[]"]
                    writer.writerow(line)

            # moves the file
            shutil.move(temp_file.name, r"cogs/poll.csv")
        else:
            await ctx.send("Start a poll to see the stats")


def setup(client):
    client.add_cog(Member(client))
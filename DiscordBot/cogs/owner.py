import discord
from discord.ext import commands

import json

###Source Code inspired from: https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
###Take cog try/except blocks

#out of class define if its the server owner
async def is_guild_owner(ctx):
    return ctx.author.id == ctx.guild.owner.id

class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, extension):
        try:
            self.client.load_extension(f"cogs.{extension}")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, extension):
        try:
            self.client.unload_extension(f"cogs.{extension}")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, extension):
        try:
            self.client.unload_extension(f"cogs.{extension}")
            self.client.load_extension(f"cogs.{extension}")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    #clear function
    @commands.command(name="clear", hidden=True)
    @commands.check(is_guild_owner)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount+1)

    #clear error handler
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please give an amount to delete")

    #command for creating a new prefix
    #for owners
    @commands.command()
    @commands.check(is_guild_owner)
    async def prefix(self, ctx, *, newprefix):
        #note the r is used for raw string literal, for file path
        with open(r"C:\Users\Kevin Lee\PycharmProjects\DiscordBot\prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = newprefix
        await ctx.send(f"New prefix is `{newprefix}`")

        with open(r"C:\Users\Kevin Lee\PycharmProjects\DiscordBot\prefixes.json", "w") as f:
            json.dump(prefixes,f,indent=4)

    #command for notifiying pin updated
    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        #handles removal
        if last_pin is None:
            await channel.send (f"Removed all pins")
        else:
            await channel.send(f"A pin has been modified in channel: {channel} on "
                               f"{last_pin.month}-{last_pin.day}-{last_pin.year}")

    #emoji updates
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, ctx, guild, before, after):
        await ctx.send(f"{guild} has updated emojis:\n"
                       f"New list of emojis: {after}")

def setup(client):
    client.add_cog(Owner(client))
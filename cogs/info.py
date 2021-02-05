import discord
from discord.ext import commands


# make sure I am doing this
def is_it_me(ctx):
    return ctx.author.id == 654142589783769117


class Info(commands.Cog):
    def __init__(self, client):

        self.client = client

    # make sure I am doing this
    def is_it_me(ctx):
        return ctx.author.id == 654142589783769117

    #server count
    @commands.command(hidden=True)
    @commands.check(is_it_me)
    async def servercount(self, ctx):
        await ctx.send(len(self.client.guilds))

    #server list lol
    @commands.command(hidden=True)
    @commands.check(is_it_me)
    async def serverlist(self, ctx):
        await ctx.trigger_typing()
        embed = discord.Embed(
            title="Server List",
            description="This is a List of servers <IBH> is in")
        sl = self.client.guilds
        for x in range(len(sl)):
            embed.add_field(name=x.name, value="<===========>", inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    async def secret(self,ctx):
        await ctx.send("||Secretty secret|| :eyes: \n\n\n\n If you found this command, DM me @ ||[REDACTED]||#||null||")
        #yahaha you found me
    @serverlist.error
    async def slerror(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            print(error)
            await ctx.send("error?")
    

def setup(client):
    client.add_cog(Info(client))
    print("info is online")

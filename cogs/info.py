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
            embed.add_field(name=sl[x], value="<===========>", inline=False)
        await ctx.send(embed=embed)
    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
      embed=discord.embed(title=f"<Insert Bot Here> Joined: `{guild.name}`", description=f"Id is {guild.id}")
      channel = self.client.get_channel(792842806291988481)
      await channel.send(embed =embed)

def setup(client):
    client.add_cog(Info(client))
    print("info is online")

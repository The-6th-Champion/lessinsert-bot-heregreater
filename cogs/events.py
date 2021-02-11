import discord
from discord.ext import commands

class Events(commands.Cog):

  def __init__(self,client):

    self.client = client
  @client.event
  async def on_guild_join(self, guild):
    channel = self.client.get_channel(792842806291988481)
    embed = discord.Embed(title="New Server Joined!!!!", description=f"<Insert Bot Here> has Joined {guild.name}.\nThe ID is {guild.id}.\nIt is owned by {guild.owner.mention}.\nIt's membercount is {guild.member_count}.", color = discord.Color(0x00ff00))
    await channel.send(embed=embed)
  @client.event
  async def on_guild_remove(self, guild):
    channel = self.client.get_channel(792842806291988481)
    embed = discord.Embed(title="Server Left <a:PensiveWobble:799822678386147388>", description=f"<Insert Bot Here> has left {guild.name}.\nThe ID is {guild.id}.\nIt is owned by {guild.owner.mention}.\nIt's membercount is {guild.member_count}.", color = discord.Color(0xff0000))
    await channel.send(embed=embed)

def setup(client):
  client.add_cog(Events(client))
  print("event is online")

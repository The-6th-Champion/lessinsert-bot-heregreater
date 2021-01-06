import discord
from discord.ext import commands

class Events(commands.Cog):

  def __init__(self,client):

    self.client = client
  @commands.Cog.listener()
  async def on_member_join(self, member):
    print("joineddddd")
    channel=764927803396718622
    await channel.send(str(member) + "has joined <Insert Server Here>! Welcome")
  @commands.Cog.listener()
  async def on_member_remove(self, member):
    channel=764927803396718622
    await channel.send(str(member) + "has left <Insert Server Here>! :sob: We will miss you....")

def setup(client):
  client.add_cog(Events(client))
  print("event is online")

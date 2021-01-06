import discord
import asyncio
from discord.ext import commands

class Say(commands.Cog):

  def __init__(self,client):

    self.client = client
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.client.user:
      pass
    elif message.author != self.client.user:
      message1 = message.content
      message1 = message1.lower()
      #await message.channel.send(message1)
      hello1 = "hello" in message1
      hello2 = "hello there" in message1
      e1 = "é" in message1
      inh1 = "<insert name here>" in message1
      link1="link" in message1
      why = "why" in message1
      howru = "how are you" in message1
      howru2 = "hru" in message1
      hbu = "hbu" in message1
      hbu2 = "how about you" in message1
      bowdown = "bow down to the 6th champion!" in message1
      if hello1 ==True and hello2 ==True:
        await message.channel.send(f"*General Kenobi*")
      elif hello1 ==True and hello2 != True:
        await message.channel.send(f"Hi {message.author.name}")
      elif e1 == True and message.author != 780928781858373672:
        await message.channel.send(f"é")
      elif inh1 ==True:
        await message.channel.send("<insert name here> is __**The Creator**__. He is also known as The 6th Champion, Da6thChamp,  and <The 6th Champion>. He developed me, and also has a support server. He is amazing. Bow down to him :person_bowing:!!!")
      elif why == True:
        await message.channel.send("why not?")
      elif link1 ==True:
        await message.channel.send("The hero of hyrule. He is resurrected a lot.")
      elif howru ==True or howru2==True:
        await message.channel.send("I am pretty good, hbu?")
      elif hbu ==True or hbu2==True:
        await message.channel.send("I am pretty good.")
      elif bowdown == True:
        await message.channel.send(file=discord.File('praisechampion.gif'))
      pass
  @commands.command()
  async def sayinfo(self,ctx):
    await ctx.send("Please do not be under the impression that this bot was made to offend. The chatting it does is merely for fun. please do not be offended by its replies, and if you do want something removed or changed, join the support server by doing `>>invite` and tell me through DMs or through <#781315950099693619>.\n-The Creator\n<insert name here>#4318")
  #@on_message.error
  #async def sayy_error(self, ctx, error, guild :discord.Guild):
    #if isinstance(error, discord.errors.Forbidden): 
        #print(f"I have no perms here{guild.name}")

def setup(client):
  client.add_cog(Say(client))
  print("say is online :)")
import discord
import asyncio
from discord.ext import commands
import firebase_admin

class Say(commands.Cog):

  def __init__(self,client):

    self.client = client
  db = firestore_admin.firestore.Client()

  @commands.command(name = "nosay", description = "This can toggle the auto-responses that are triggered from certain phrases like\n \'why\' and \'why not\'\n and\n \'Hello\' and \'Hi <name>")
  @commands.has_permissions(administrator = True)
  async def nosay(self, ctx):
    ref = db.collection("guilds").doc(message.guild.id)
    doc = ref.get()
    data = doc.to_dict()
    if data.toggle_say == True:
      doc.update({
        "toggle_say" : False
      })
    elif data.toggle_say == False:
      doc.update({
        "toggle_say" : True
      }) 
    else:
      doc.update({
        "toggle_say" : False
      })

  @commands.Cog.listener()
  async def on_message(self, message):
    
    ref = db.collection("guilds").doc(message.guild.id)
    doc = ref.get()
    data = doc.to_dict()
    if data.toggle_say == True:
      #send message
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
        #why = "why" in message1
        #howru = "how are you" in message1
        #howru2 = "hru" in message1
        #hbu = "hbu" in message1
        #hbu2 = "how about you" in message1
        bowdown = "bow down to the 6th champion!" in message1
        praisechamp = "praise the 6th champion!" in message1
        bowdownl = "bow down to link" in message1
        ytea = "yorkshire tea" in message1
        if hello1 ==True and hello2 ==True:
          await message.channel.send(f"*General Kenobi*")
        elif hello1 ==True and hello2 != True:
          await message.channel.send(f"Hi {message.author.name}")
        elif e1 == True and message.author != 780928781858373672:
          await message.channel.send(f"é")
        elif inh1 ==True:
          await message.channel.send("<insert name here> is __**The Creator**__. He is also known as The 6th Champion, Da6thChamp,  and <The 6th Champion>. He developed me, and also has a support server. He is amazing. Bow down to him :person_bowing:!!!")
        #elif why == True:
          #await message.channel.send("why not?")
        elif link1 ==True and bowdownl ==False:
          await message.channel.send("The hero of hyrule. He is resurrected a lot.")
        #elif howru ==True or howru2==True:
          #await message.channel.send("I am pretty good, hbu?")
        #elif hbu ==True or hbu2==True:
          #await message.channel.send("I am pretty good.")
        #things have been commented out to decrease annoying ness
        elif bowdown == True or praisechamp == True:
          await message.channel.send("It must be done!")
          await message.channel.send(file=discord.File('./gifs/praisechampion.gif'))
        elif bowdownl ==True and link1 == True:
          await message.channel.send("smh no")
        elif ytea == True:
          await message.channel.send("Yorkshire Tea is amazing")
          await message.channel.send("<:yorkshire_1:798737240313561128><:yorkshire_2:798737240502435851>\n<:yorkshire_3:798737240112889888><:yorkshire_4:798737240276598814>")
    else:
      pass
  @commands.command(description="message from the Creator about the bots chatting ability")
  async def sayinfo(self,ctx):
    await ctx.send("Please do not be under the impression that this bot was made to offend. The chatting it does is merely for fun. please do not be offended by its replies, and if you do want something removed or changed, join the support server by doing `>>invite` and tell me through DMs or through <#781315950099693619>.\n-The Creator\n<insert name here>#4318")


def setup(client):
  client.add_cog(Say(client))
  print("say is online :)")

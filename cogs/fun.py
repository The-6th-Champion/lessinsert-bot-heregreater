from bot import disciple
import discord
from discord.ext import commands
import pyrebase

config = {
    "apiKey": "AIzaSyCWPSVy-1jPpSup_mNm2wNzzyzwnM4tn6M",
    "authDomain": "less-insert-bot-here-greater.firebaseapp.com",
    "databaseURL": "https://less-insert-bot-here-greater-default-rtdb.firebaseio.com",
    "projectId": "less-insert-bot-here-greater",
    "storageBucket": "less-insert-bot-here-greater.appspot.com",
    "messagingSenderId": "328700534390",
    "appId": "1:328700534390:web:f2b11d24e439f924098957",
    "measurementId": "G-79TMJX9X3G"
}
#firebase = firebase.FirebaseApplication("https://less-insert-bot-here-greater-default-rtdb.firebaseio.com/")
firebase = pyrebase.initialize_app(config)
db=firebase.database()
class Fun(commands.Cog):

  def __init__(self,client):

    self.client = client
  @commands.command(hidden = True, aliases = ["rickroll"])
  async def rr(self, ctx):
    embed = discord.Embed(title="Wow!", description = "you found this!")
    embed.set_image(url = "https://cdn.discordapp.com/attachments/455236204477022208/786274088247099433/wheres_waldo.png")
    await ctx.send(embed = embed)
  #say command: repeats arguments added
  @commands.command()
  async def say(self, ctx, *, message=None):
      if message == None:
          await ctx.send("Please Provide a message! ex `.say message`")
      await ctx.send(message)
  @commands.command()
  async def bowdown(self, ctx, *, message=None):
    if message == None:
      await ctx.send("Please recite the pledge: I bow down to my holy lord, The 6th Champion, and surrender myself to His cause")
    elif message != "I bow down to my holy lord, The 6th Champion, and surrender myself to His cause":
      await ctx.send("Please properly recite the pledge: I bow down to my holy lord, The 6th Champion, and surrender myself to His cause")
    else:
      db.push(str(ctx.author.id))
      
  @commands.command()
  async def disciple(self, ctx, *, message=None):
    disciple = False
    ids = db.get()
    for i in ids.each():
      await ctx.send(i.val())
    await ctx.send(ids.val())
    with open("./data/disciples.txt", "r") as f:
      parse = f.read().split("\n")
    if str(ctx.author.id) == '654142589783769117':
      await ctx.send(":open_mouth:...it is....an honor....it is actually you. :person_bowing: all hail The true **6th Champion**.")
    elif disciple == True:
      await ctx.send("You are a verified disciple of the 6th Champion!")
    else:
      await ctx.send("You have not been verfied as a disciple of the 6th Champion")
    """
    elif str(ctx.author.id) == "347145371140489218":
      await ctx.send("Greetings, my **Flamekeeper**, Defender of the 6th Champion")
    """
    

def setup(client):
  client.add_cog(Fun(client))
  print("fun is online")
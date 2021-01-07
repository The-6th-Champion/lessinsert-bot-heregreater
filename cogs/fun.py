from discord import client, guild
from discord.member import Member
from bot import disciple
import discord
from discord.ext import commands
import pyrebase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

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
dbids = db.get()
ids = []
for i in dbids.each():
  ids.append(i.val())
isChattingClever = False
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
    elif str(ctx.author.id) not in ids:
      db.push(str(ctx.author.id))
      ids.append(str(ctx.author.id))
      if ctx.guild.id == 764927590070353940:
        role = discord.utils.get(ctx.guild.roles, name="<Disciple>")
        user = ctx.message.author
        await Member.add_roles(user, role)
        await ctx.send("You have become one with the 6th Champion!")
      else:
        await ctx.send("You have become one with the 6th Champion!")
    else:
      await ctx.send(ctx.author.guild.id)
      await ctx.send("You have already become one with the 6th Champion!")

      
  @commands.command()
  async def disciple(self, ctx, *, message=None):
    if str(ctx.author.id) == '654142589783769117':
      await ctx.send(":open_mouth:...it is....an honor....it is actually you. :person_bowing: all hail The true **6th Champion**.")
    elif str(ctx.author.id) == "347145371140489218":
      await ctx.send("Greetings, my **Flamekeeper**, Defender of the 6th Champion")
    elif str(ctx.author.id) in ids:
      await ctx.send("You are a verified disciple of the 6th Champion!")
    else:
      await ctx.send("You have not been verfied as a disciple of the 6th Champion")
  @commands.command()
  async def startchat(self, ctx, *, message=None):
    global driver
    global text_area
    global isChattingClever
    if isChattingClever == False:
      isChattingClever = True
      await ctx.send("Getting chat ready...")
      options = webdriver.ChromeOptions()
      options.add_argument("--headless")
      options.add_argument("--disable-dev-shm-usage")
      options.add_argument("--no-sandbox")
      driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
      driver.get('https://www.cleverbot.com/')
      button = driver.find_element_by_id('noteb')
      button.click()
      text_area = driver.find_element_by_xpath('//*[@id="avatarform"]/input[1]')
      await ctx.send("Chat ready! Say something using >>tellbot")
  @commands.command()
  async def tellbot(self, ctx, *, message=None):
    if isChattingClever == True:
      text_area.send_keys(message)
      text_area.send_keys(Keys.RETURN)
      time.sleep(5)
      botresponse = driver.find_element_by_xpath("//*[@id='line1']/span[1]").text
      await ctx.send(botresponse)
  @commands.command()
  async def endchat(self, ctx, *, message=None):
    global isChattingClever
    if isChattingClever == True:
      isChattingClever = False
      await driver.close()
      await ctx.send("Chat ended!")
def setup(client):
  client.add_cog(Fun(client))
  print("fun is online")

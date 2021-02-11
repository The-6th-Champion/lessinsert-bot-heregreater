from inspect import isclass
from discord import client, guild
from discord.ext.commands import context
from discord.ext.commands import bot
from discord.ext.commands.bot import Bot
from discord.member import Member
from bot import disciple
import discord
from discord.ext import commands
import firebase_admin
from pyppeteer import launch
import asyncio
import time

dbids = db.get()
ids = []
for i in dbids.each():
  ids.append(i.val())
isChattingClever = False
class Fun(commands.Cog):
  
  def __init__(self,client):

    self.client = client
  @commands.command(hidden = True)
  async def rr(self, ctx):
    message = ctx.message
    embed = discord.Embed(title="Wow!", description = "you found this!\nFind Waldo in this picture.")
    embed.set_image(url = "https://cdn.discordapp.com/attachments/455236204477022208/786274088247099433/wheres_waldo.png")
    await message.delete()
    await ctx.send(embed = embed)
  #say command: repeats arguments added
  @commands.command(description="Says message back to you. \n\n- Please use this command according to your server rules.\n- This command is not meant to be used to target or hurt someone, so please do not use it for that.\n\n\tExample\n\t\t-  User: \>>say Hello\n\t\t-  Bot: Hello")
  async def say(self, ctx, *, message=None):
      realmessage = ctx.message 
      if message == None:
          await ctx.send("Please Provide a message! ex `.say message`")
      else:
          await realmessage.delete()
          await ctx.send(message)
  @commands.command(description="This is a command that will add you to the 6th champion disciple club. You can check your status with the `disciple` command. This is for fun, I do not mean to offend any religious beliefs. Have fun, and join the club!")
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
  @commands.command(description="This is a way to check if you are a follower of the 6th champion. dont worry this is a joke command, along with `bowdown` and I do not mean to offend any religious beliefs. Have fun, and join the club!")
  async def disciple(self, ctx, *, message=None):
    if str(ctx.author.id) == '654142589783769117':
      await ctx.send(":open_mouth:...it is....an honor....it is actually you. :person_bowing: all hail The true **6th Champion**.")
    elif str(ctx.author.id) == "347145371140489218":
      await ctx.send("Greetings, my **Flamekeeper**, Defender of the 6th Champion")
    elif str(ctx.author.id) in ids:
      await ctx.send("You are a verified disciple of the 6th Champion!")
    else:
      await ctx.send("You have not been verfied as a disciple of the 6th Champion")
  @commands.command(aliases=["sc"])
  async def startchat(self, ctx, *, message=None):
    global browser
    global page
    global isChattingClever
    if not isChattingClever:
      isChattingClever = True
      await ctx.send("Getting chat ready...")
      browser = await launch(options={'args': ['--no-sandbox']})
      page = await browser.newPage()
      await page.goto("https://www.pandorabots.com/mitsuku/")
      await page.click("#pb-widget > div > div > div.pb-widget__description > div.pb-widget__description__chat-now > button")
      time.sleep(5)
      await ctx.send("Chat ready! Say something using `>>tellbot` or `>>tb`")
    else:
      await ctx.send("You are already chatting with me!")
  @commands.command(name = "tellbot", aliases=["tb"])
  async def tellbot(self, ctx, *, message=None):
    if isChattingClever == True:
      async with ctx.typing():
        await page.type("#pb-widget-input-field", message)
        await page.keyboard.press("Enter")
        #time.sleep(0.5)
        thelist = await page.querySelectorAll(".pb-message > div > div")
        botresponse = await page.evaluate('(element) => element.textContent', thelist[len(thelist)-1])
        while botresponse == message:
          thelist = await page.querySelectorAll(".pb-message > div > div")
          botresponse = await page.evaluate('(element) => element.textContent', thelist[len(thelist)-1])
        if "https://www.kuki.ai/" in botresponse:
          botresponse = botresponse.replace("https://www.kuki.ai/", "<insert website here>")
        elif botresponse == "Try sending mail to Pandorabots (info@kuki.bot)":
          botresponse = "Send messages for feedback to <#781315950099693619>"
        elif "kuki" in botresponse.lower():
          botresponse = botresponse.replace("Kuki", "<Insert bot here>")
        elif "pandorabots" in botresponse.lower():
          botresponse = botresponse.replace("Pandorabots", "The 6th Champion")
        await ctx.send(botresponse)
    else:
      await ctx.send("Chat not active! Run `>>startchat` to get started and `>>endchat` to end the conversation!")
  @commands.command(aliases=['ec'])
  async def endchat(self, ctx, *, message=None):
    global isChattingClever
    global browser
    if isChattingClever == True:
      isChattingClever = False
      await browser.close()
      await ctx.send("Chat ended")
    else:
      await ctx.send("You haven't started a conversation with me. `>>startchat` to start one now!")
def setup(client):
  client.add_cog(Fun(client))
  print("fun is online")


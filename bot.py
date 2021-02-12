import discord
from discord.ext import commands
import os
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
import json



configvars = {
    "type": "service_account",
    "project_id": os.environ.get("project_id"),
    "private_key": os.environ.get('private_key').replace('\\n', '\n'),
    "client_email": os.environ.get("client_email"),
    "client_id": os.environ.get("client_id"), 
    "auth_uri": os.environ.get("auth_uri"),
    "token_uri": os.environ.get("token_uri"),
    "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.environ.get("client_x509_cert_url")
}

json.dump(configvars, open('stuffs.json', 'w'))
cred = credentials.Certificate('stuffs.json')
default_app = firebase_admin.initialize_app(cred)
intents = discord.Intents.default()
db = firestore.client()
def get_prefix(client, message : discord.Message): ##first we define get_prefix
    doc_ref = db.collection("guild").document(str(message.guild.id))
    doc = doc_ref.get()
    data = doc.to_dict()
    if data["prefix"] == None:
        doc_ref.set({
            "prefix" : ">>"
        })
        data = doc_ref.get().to_dict()

    return str(data["prefix"]) #recieve the prefix for the guild id given

intents.guilds = True
intents.members = True
client = commands.Bot(command_prefix=(get_prefix), intents = intents, case_insensitive = True)
client.remove_command("help")
TOKEN = TOKEN = os.environ.get("TOKEN")


#cred = credentials.Certificate('stuffs.json')
#default_app = firebase_admin.initialize_app(cred)

#work?


# make sure I am doing this
def is_it_me(ctx):
    return ctx.author.id == 654142589783769117


# Help
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color(0x9ef), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

client.help_command = MyHelpCommand()




# Commands
@client.command(name = "ping", aliases=["pong"],description="Returns the latency of the bot.")
async def ping(ctx):
    embed = discord.Embed(
        title="PING",
        description=
        f":ping_pong: Pong! The ping is **{round(client.latency *1000)}** milliseconds!",
        color=0x00ff00)
    await ctx.send(embed=embed)

@client.command(hidden=True)
async def credits(ctx):
    em = discord.Embed(
        title="Credits",
        description=
        "Creator/Owner: <insert name here>#XXXX\nProfile Picture: <insert name here>#XXXX\nBig helpers and contributers: ElectronDev and Fumseck of Zeldevs, Isukali"
    )
    em.set_footer(text = "If you found this command, have a cookie :cookie: lol. :)")
    await ctx.send(embed=em)

#prefix command. gives bot prefix
@client.command(name = "prefix", description="Returns the prefix of the bot. \nif you add an argument, it changes the bot's prefix.`BETA` (custom prefix doesnt work yet)")
async def prefix(ctx):
    embed1 = discord.Embed(
        title='Prefix',
        description=f"This Bot's prefix is `>>`",
        color=discord.Color.blue())

#change prefix
@client.command(name = "setprefix", description="changes prefix. You need Admin Permission")
@commands.has_permissions(administrator = True)
async def setprefix(ctx, prefix = None):
    embed2 = discord.Embed(
        title='Prefix',
        description=f"This Bot's prefix has been changed to `{prefix}`",
        color=discord.Color.green())
    doc_ref = db.collection('guild').document(str(ctx.guild.id))

    if prefix == None:
        await ctx.send("Please provide a prefix")
    else:
        doc_ref.set({
            'prefix': prefix
        }, merge = True)
        await ctx.send(embed=embed2)

@client.command(hidden=True)
@commands.check(is_it_me)
async def sudosay(ctx,type,  location, *, content):
    location = location.replace("<", "")
    location = location.replace(">", "")
    location = location.replace("@!", "")
    location = location.replace("#", "")
    if type =="user":
          channel = client.get_user(int(location))
    elif type =="channel":
          channel = client.get_channel(int(location))
    await channel.send(content)
    await ctx.send(f"Sent to {channel.name} successfully.")

@sudosay.error
async def ssay_error(error, ctx):
    em1 = discord.Embed(title = "Sudosay Command", description="`>>sudosay <channel | user> <id of user/channel> <content>", color = discord.Color(0xf00))
    if isinstance(error, discord.ext.commands.errors.BadArgument): 
        await ctx.send("honestly this is a BadArgument Error",embed=em1)
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions): 
        await ctx.send("This bot cannot send messages here.", embed = em1)
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument, embed= em1): 
        await ctx.send("are you missing something?")
    else:
        await ctx.send(f"```\n{error}\n\nPlease try again and stuff.", embed = em1)
        raise error

#prefix reset for all servers.....danger :)
@client.command()
@commands.check(is_it_me)
async def mememe(ctx):
    for guild in client.guilds:
        doc_ref = db.collection("guild").document(str(guild.id))
        doc_ref.set({
            "prefix" : ">>",
            "toggle_say" : True
        }, merge = True)
    await ctx.send("done?")
            
@client.event
async def on_guild_join(guild):
    doc_ref = db.collection("guild").document(str(guild.id))
    doc_ref.set({
            "prefix" : ">>",
            "toggle_say" : True
        }, merge = True)
    channel = client.get_channel(792842806291988481)
    embed = discord.Embed(title="New Server Joined!!!!", description=f"<Insert Bot Here> has Joined {guild.name}.\nThe ID is {guild.id}.\nIt is owned by {guild.owner.mention}.\nIt's membercount is {guild.member_count}.", color = discord.Color(0x00ff00))
    await channel.send(embed=embed)
@client.event
async def on_guild_remove(guild):
    channel = client.get_channel(792842806291988481)
    embed = discord.Embed(title="Server Left <a:PensiveWobble:799822678386147388>", description=f"<Insert Bot Here> has left {guild.name}.\nThe ID is {guild.id}.\nIt is owned by {guild.owner.mention}.\nIt's membercount is {guild.member_count}.", color = discord.Color(0xff0000))
    await channel.send(embed=embed)



#Say
#
#

@client.command(name = "togglesay", description = "This can toggle the auto-responses that are triggered from certain phrases like\n \'why\' and \'why not\'\n and\n \'Hello\' and \'Hi <name>")
@commands.has_permissions(administrator = True)
async def togglesay(ctx):
    ref = db.collection("guild").document(str(message.guild.id))
    doc = ref.get()
    data = doc.to_dict()
    if data["toggle_say"] == True:
        doc.set({
        "toggle_say" : False
        }, merge = True)
        await ctx.send("The say function is now disabled")
    elif data.toggle_say == False:
        doc.set({
        "toggle_say" : True
        }, merge = True)
        await ctx.send("The say function is now enabled")

@client.event
async def on_message(message):
    ref = db.collection("guild").document(str(message.guild.id))
    doc = ref.get()
    data = doc.to_dict()
    if data{"toggle_say"} == True:
        #send message
        if message.author == client.user:
            pass
        elif message.author != client.user:
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
            elif why == True:
                await message.channel.send("why not?")
            elif link1 ==True and bowdownl ==False:
                await message.channel.send("The hero of hyrule. He is resurrected a lot.")
            elif howru ==True or howru2==True:
                await message.channel.send("I am pretty good, hbu?")
            elif hbu ==True or hbu2==True:
                await message.channel.send("I am pretty good.")
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
@client.command(description="message from the Creator about the bots chatting ability")
async def sayinfo(ctx):
    await ctx.send("Please do not be under the impression that this bot was made to offend. The chatting it does is merely for fun. please do not be offended by its replies, and if you do want something removed or changed, join the support server by doing `>>invite` and tell me through DMs or through <#781315950099693619>. You can also discable the auto messages with the togglesay command.\n-The Creator\n<insert name here>#4318")


# Cog stuff
cogs = ['cogs.utils', 'cogs.moderation', 'cogs.fun',  'cogs.info'] #'cogs.events', 'cogs.say',

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as e:
        print(f"e1: Could not load cog {cog}:{str(e)}")


# alerts if bot is ready
@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="404: <insert movie here> not found"))
    print("<Bot is Ready.>")


#Load cog
@client.command(hidden=True)
@commands.check(is_it_me)
async def loadcog(ctx, cogname=None, hidden=True):
    if cogname is None:
        await ctx.send("-_-")
        return
    try:
        client.load_extension(cogname)
    except Exception as e:
        print(f"Could not load cog {cog}:{str(e)}")
        await ctx.send("-_-")
    else:
        print('Loaded Cog Succesfully')
        await ctx.send(f"{cog} is online.")


#Unload cog
@client.command(hidden=True)
@commands.check(is_it_me)
async def unloadcog(ctx, cogname=None, hidden=True):
    if cogname is None:
        return
        await ctx.send("-_-")
    try:
        client.unload_extension(cogname)
    except Exception as e:
        print(f"Could not unload cog {cog}:{str(e)}")
        await ctx.send("-_-")
    else:
        print('Unloaded Cog Succesfully')
        await ctx.send(f"{cog} is offline.")


        
client.run(TOKEN)
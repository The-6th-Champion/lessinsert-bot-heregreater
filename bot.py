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
    await ctx.send(embed = embed1)

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
@setprefix.error
async def sp_error(error, ctx):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("You are not an **Administrator**, or you don't have the **Administrator** permission")
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


    for guild in client.guilds:
        doc_ref = db.collection("guild").document(str(guild.id))
        doc_ref.set({
            "prefix" : ">>"
        }, merge = True)
    await ctx.send("done?")
            
@client.event
async def on_guild_join(guild):
    doc_ref = db.collection("guild").document(str(guild.id))
    doc_ref.set({
            "prefix" : ">>"
        }, merge = True)
    channel = client.get_channel(792842806291988481)
    embed = discord.Embed(title="New Server Joined!!!!", description=f"<Insert Bot Here> has Joined {guild.name}.\nThe ID is {guild.id}.\nIt is owned by {guild.owner.mention}.\nIt's membercount is {guild.member_count}.", color = discord.Color(0x00ff00))
    await channel.send(embed=embed)
@client.event
async def on_guild_remove(guild):
    channel = client.get_channel(792842806291988481)
    embed = discord.Embed(title="Server Left <a:PensiveWobble:799822678386147388>", description=f"<Insert Bot Here> has left {guild.name}.\nThe ID is {guild.id}.\nIt is owned by {guild.owner.mention}.\nIt's membercount is {guild.member_count}.", color = discord.Color(0xff0000))
    await channel.send(embed=embed)


# Cog stuff
cogs = ['cogs.utils', 'cogs.moderation', 'cogs.funclone',  'cogs.info'] #'cogs.events', 'cogs.say',

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
    await client.get_channel(770401102981627924).send("im online")
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

#Reload cog
@client.command(hidden=True)
@commands.check(is_it_me)
async def reloadcog(ctx, cogname = None, hidden = True):
    if cogname is None:
        return
        await ctx.send("-_-")
    try:
        client.unload_extension(cogname)
        client.load_extension(cogname)
    except Exception as e:
        print(f"Could not reload cog {cog}:{str(e)}")
        await ctx.send("-_-")
    else:
        print('reloaded Cog Succesfully')
        await ctx.send(f"{cog} is restarted.")


#funny joke
@client.command(description="This is a command that will add you to the 6th champion disciple club. You can check your status with the `disciple` command. This is for fun, I do not mean to offend any religious beliefs. Have fun, and join the club!")
async def bowdown(self, ctx, *, message=None):
    ids = db.collection("disciples").get()
    doc_ref = db.collection("disciples").document(str(ctx.author.id))
    if message == None:
        await ctx.send("Please recite the pledge: I bow down to my holy lord, The 6th Champion, and surrender myself to His cause")
    elif message != "I bow down to my holy lord, The 6th Champion, and surrender myself to His cause":
        await ctx.send("Please properly recite the pledge: I bow down to my holy lord, The 6th Champion, and surrender myself to His cause")
    elif str(ctx.author.id) not in ids:
        doc_ref.set(merge = True)
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
@client.command(description="This is a way to check if you are a follower of the 6th champion. dont worry this is a joke command, along with `bowdown` and I do not mean to offend any religious beliefs. Have fun, and join the club!")
async def disciple(self, ctx, *, message=None):
    ids = db.collection("disciples").get()
    if str(ctx.author.id) == '654142589783769117':
        await ctx.send(":open_mouth:...it is....an honor....it is actually you. :person_bowing: all hail The true **6th Champion**.")
    elif str(ctx.author.id) == "347145371140489218":
        await ctx.send("Greetings, my **Flamekeeper**, Defender of the 6th Champion")
    elif str(ctx.author.id) in ids:
        await ctx.send("You are a verified disciple of the 6th Champion!")
    else:
        await ctx.send("You have not been verfied as a disciple of the 6th Champion look at the `bowdown` command")
client.run(TOKEN)
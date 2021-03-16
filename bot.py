import discord
from discord.ext import commands
import os
import asyncio
from fb_init import db


def get_prefix(client, message : discord.Message): ##first we define get_prefix
    try:
        doc_ref = db.collection("guild").document(str(message.guild.id))
        doc = doc_ref.get()
        data = doc.to_dict()
        if data["prefix"] == None:
            doc_ref.set({
                "prefix" : "ib"
            })
            data = doc_ref.get().to_dict()
        prefix_list = []
        return commands.when_mentioned_or(str(data["prefix"]), "ib")(client,message)
    except AttributeError: return commands.when_mentioned_or("ib")(client, message) #recieve the prefix for the guild id given
intents = discord.Intents.default()


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
        e.set_footer(text = f"Do `>>prefix` to see the custom prefix")
        await destination.send(embed=e)

client.help_command = MyHelpCommand()




# Commands
@client.command(aliases = ["setp"], description = "change the presence of the bot. \n types: streaming, playing, listening or watching")
@commands.check(is_it_me)
async def setpresence(ctx, type1, *, presence):
    if type1 ==  "streaming": await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=presence))
    elif type1 ==  "playing": await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=presence))
    elif type1 ==  "listening": await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=presence))
    elif type1 ==  "watching": await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=presence))
    else: await ctx.send("try again"); return
    await ctx.send(f"Done! set presence to **{type1.capitalize()} {presence}**")

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
        "Creator/Owner: The 6th Champion#3981\nProfile Picture: Isukali#XXXX\nBig helpers and contributers: Isukali"
    )
    em.set_footer(text = "If you found this command, have a cookie :cookie: lol. :)")
    await ctx.send(embed=em)

#prefix command. gives bot prefix
@client.command(name = "prefix", description="Returns the prefix of the bot. \nif you add an argument, it changes the bot's prefix.`BETA` (custom prefix doesnt work yet)")
async def prefix(ctx):
    try:
        doc_ref = db.collection("guild").document(str(ctx.guild.id))
        data = doc_ref.get().to_dict()
        data1 = data["prefix"]
        embed1 = discord.Embed(
            title='Prefix',
            description=f"This Bot's prefix is `{data1}`",
            color=discord.Color.blue())
        await ctx.send(embed=embed1)
    except:
        embed2 = discord.Embed(
            title='Prefix',
            description="This Bot's prefix is `>>`",
            color=discord.Color.blue())
        await ctx.send(embed=embed2)

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
            name="For >>help and >>invite"))
    await client.get_channel(770401102981627924).send("im online")
    print("<Bot is Ready.>")

#Error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound): 
        await ctx.send("This command doesnt exist. Try again!")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Make sure you and I both have the permissions need for this command.")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("You are missing a required parameter to this command")
    elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
        await ctx.send("This command doesnt work in a DM.")
    else:
        raise error

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
        client.reload_extension(cogname)
    except Exception as e:
        print(f"Could not reload cog {cog}:{str(e)}")
        await ctx.send("-_-")
    else:
        print('reloaded Cog Succesfully')
        await ctx.send(f"{cog} is restarted.")
        
client.run(TOKEN)
import discord
from discord.ext import commands
import webserver
from webserver import keep_alive
import os
import asyncio

client = commands.Bot(command_prefix=commands.when_mentioned_or('>>'))
client.remove_command("help")
TOKEN = TOKEN = os.environ.get("TOKEN")


# make sure I am doing this
def is_it_me(ctx):
    return ctx.author.id == 654142589783769117


#help command
@client.group(name="help", invoke_without_command=True)
async def help(ctx):
    embed1 = discord.Embed(
        title="Help",
        description=
        "Use `>>help [command]` for more info on each command.\n\n **Note: anything in `<>` is a necassary argument, anything in `[]` is optional**",
        color=discord.Color(0x9ef))
    embed1.add_field(
        name="Moderation",
        value="""
- `kick` kicks user from server
- `ban` bans user from server
- `unban` unbans user from server
- `clear` clears a certain amount of messages from the current channel""")
    embed1.add_field(
        name="Utility",
        value="""
- `invite` Gives invite link of bot and invite link of support server
- `prefix` returns prefix, which is **`>>`**
- `userinfo` returns info on on the specified user
- `roleinfo` gives the ID of the specified role
- `upvote` gives the upvote link of the bot""")
    embed1.add_field(
        name="Other",
        value="""
- `help` shows the help message
- `ping` gives the latency of the bot""",
        inline=False)
    embed1.add_field(
        name="Fun",
        value="""
- `say` returns ``<message>`` back to the chat. """)
    embed1.add_field(
        name="Important",
        value=
        """- `status` returns with message if bot is online. If it doesn't, It isnt online lol :)
        - `sayinfo` Returns message from the creator! please look at this in your spare time.""",
          inline=False)
    embed1.set_thumbnail(url = client.user.avatar_url)
    await ctx.send(embed=embed1)


@help.command()
async def kick(ctx):
    em = discord.Embed(
        title="Kick Command",
        description=
        "`>>kick | k <user> [reason]`\t Kicks a user from the server.",
        color=discord.Color(0x9ef))
    em.add_field(name="Permissions", value="kick users is required")
    await ctx.send(embed=em)


@help.command()
async def ban(ctx):
    em = discord.Embed(
        title="Ban Command",
        description="`>>ban <user> [reason]`\t Bans a user from the server.",
        color=discord.Color(0x9ef))
    em.add_field(name="Permissions", value="ban users is required")
    await ctx.send(embed=em)


@help.command()
async def clear(ctx):
    em = discord.Embed(
        title="Clear Command",
        description=
        "`>>clear <number of messages>`\t clears a number of messages from the channel.\n\n\t- it deletes `<number of messages>` and the command message automatically, so don't be alarmed if the success message says it deleted one too many messages\n\t- if you dont supply any number, the bot will just delete your command message",
        color=discord.Color(0x9ef))
    em.add_field(name="Permissions", value="manage messages is required")
    await ctx.send(embed=em)


@help.command()
async def unban(ctx):
    em = discord.Embed(
        title="Unban Command",
        description="`>>unban <user#discrim>`\t unbans a user from the server.",
        color=discord.Color(0x9ef))
    em.add_field(name="Permissions", value="ban users is required")
    await ctx.send(embed=em)


@help.command()
async def invite(ctx):
    em = discord.Embed(
        title="Invite Command",
        description=
        "`>>invite`\t Gives the invite link of the bot, and the invite link of the support server.",
        color=discord.Color(0x9ef))
    await ctx.send(embed=em)


@help.command()
async def prefix(ctx):
    em = discord.Embed(
        title="Prefix Command",
        description="`>>prefix`\t Returns the prefix of the bot.",
        color=discord.Color(0x9ef))
    await ctx.send(embed=em)


@help.command()
async def userinfo(ctx):
    em = discord.Embed(
        title="Userinfo Command",
        description=
        "`>>userinfo <user>`\t Gives the Name, discriminator, User ID, and if the specified user is a bot.",
        color=discord.Color(0x9ef))
    await ctx.send(embed=em)


@help.command()
async def ping(ctx):
    em = discord.Embed(
        title="Ping Command",
        description="`>>ping`\t Returns the latency of the bot.",
        color=discord.Color(0x9ef))
    await ctx.send(embed=em)


@help.command()
async def say(ctx):
    em = discord.Embed(
        title="Say Command",
        description=
        "`>>say <messsage>`\t Says message back to you. \n\n- Please use this command according to your server rules.\n- This command is not meant to be used to target or hurt someone, so please do not use it for that.\n\n\tExample\n\t\t-  User: \>>say Hello\n\t\t-  Bot: Hello",
        color=discord.Color(0x9ef))
    await ctx.send(embed=em)


@help.command()
async def roleinfo(ctx):
    em = discord.Embed(
        title="Roleinfo Command",
        description=
        "`>>roleinfo <role>`\t Gives the Role ID of the specified role.",
        color=discord.Color(0x9ef))
    await ctx.send(embed=em)


@help.command()
async def status(ctx):
    em = discord.Embed(
        title="Status Command",
        description=
        "`>>status`\t If the bot is online, It will give a message. If it isn't, it will not say anything.",
        color=discord.Color(0x9ef))
    await ctx.send(embed=em)


@help.command()
async def rr(ctx):
    em = discord.Embed(
        title="[REDACTED] **Hidden** Command :eyes:",
        description="`>>[READCTED]`\t returns an image [REDACTED] lmao :)",
        color=discord.Color(0x0f0))
    await ctx.send(embed=em)


@help.command()
async def credits(ctx):
    em = discord.Embed(
        title="Credits **Hidden** Command :eyes:",
        description=
        "`>>credits`\t Gives the credits of the bot.\n\n If you are not on here, and you feel like you should be, go to the support server and contact The Creator...",
        color=discord.Color(0x0f0))
    await ctx.send(embed=em)


@help.command(aliases=["mod"])
async def moderation(ctx):
    em = discord.Embed(
        title="Moderation Command Group",
        description="`>>kick`\n`>>ban`\n`>>clear`\n`>>unban`",
        color=discord.Color(0x0f0))
    await ctx.send(embed=em)


@help.command(aliases=["util"])
async def utility(ctx):
    em = discord.Embed(
        title="Utility Command Group",
        description="`>>userinfo`\n`>>invite`\n`>>prefix`\n`>>roleinfo`",
        color=discord.Color(0x0f0))
    await ctx.send(embed=em)


@help.command()
async def fun(ctx):
    em = discord.Embed(
        title="FunCommand Group",
        description="`>>say`\n`>>[REDACTED due to being hidden]`",
        color=discord.Color(0x0f0))
    await ctx.send(embed=em)


@help.command()
async def other(ctx):
    em = discord.Embed(
        title="Moderation Command Group",
        description="`>>help`\n`>>status`\n`ping`",
        color=discord.Color(0x0f0))
    await ctx.send(embed=em)


@help.command()
async def upvote(ctx):
    em = discord.Embed(
        title="Upvote Command",
        description="`>>upvote` Gives the link to upvote the Bot",
        color=discord.Color(0x0f0))
    await ctx.send(embed=em)

@help.command()
async def sayinfo(ctx):
  em = discord.Embed(title="Say Info Message", description="`>>sayinfo` message from the Creator about the bots chatting ability")
  await ctx.send(embed=em)

# Cog stuff
cogs = ['cogs.events', 'cogs.utils', 'cogs.moderation', 'cogs.fun', 'cogs.say', 'cogs.info']

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


# ping commnd: ping, response time ig
@client.command(aliases=["pong"])
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
        "Creator/Owner: <insert name here>#XXXX\nProfile Picture: <insert name here>#XXXX\nIf you found this command, have a cookie :cookie: lol. :)"
    )
    await ctx.send(embed=em)


#@client.event
#async def on_message(message):
#  embed = discord.Embed(title = 'Prefix', description = f"This Bot's prefix is #`>>`", color = discord.Color.blue())
#  if client.user.mentioned_in(message):
#      await message.channel.send("Hmmm?", embed=embed)


@client.command(hidden=True, aliases=['ss'])
@commands.check(is_it_me)
async def sudosay(ctx, channel: discord.TextChannel, *, message):
    await channel.send(message)


keep_alive()
client.run(TOKEN)

# \t- it deletes `<number of messages>` and the command message automatically, so don't be alarmed if the success message says it deleted one too many messages
#  \t- if you dont supply any number, the bot will just delete your command message
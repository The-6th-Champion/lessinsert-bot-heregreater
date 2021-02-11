import discord
import asyncio
from discord.ext import commands
class Moderation(commands.Cog):

  def __init__(self, client):
    self.client = client


  #kick command: kicks user
  @commands.command(aliases = ["k"], description="Kicks a user from the server.")
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member, *, reason = None):
    #embed for server
    embed1 = discord.Embed(title = 'Kicked', description = f"A user was kicked from this server", color = discord.Color.light_gray())
    embed1.add_field(name = member, value = f"- {member.name} was successfully kicked from this server")
    embed1.add_field(name = "Reason", value = f"{reason}", inline = False)
    embed1.set_thumbnail(url =  ctx.guild.icon_url)
    #embed for user
    embed2 = discord.Embed(title = 'Kicked', description = f"You were kicked from {ctx.guild.name}", color = discord.Color.light_gray())
    embed2.add_field(name = "Reason", value = f"{reason}", inline = False)
    embed2.set_thumbnail(url =  ctx.guild.icon_url)
    
    await member.send(embed=embed2)
    await member.kick(reason = reason)
    await ctx.send(embed = embed1)
  @kick.error
  async def kick_error(self, ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument): 
        await ctx.send("Please specify a **valid** user!")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("You need the **kick members** permission")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Please specify a **valid** user!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument): 
        await ctx.send("Please specify a **valid** user!")
    else:
        raise error



    #ban command: bans user
  @commands.command(aliases = ["b"], description="Bans a user from the server.")
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member, *, reason = None):
    #embed for server
    embed1 = discord.Embed(title = 'Banned :hammer:', description = f"A user was banned from this server", color = discord.Color.darker_gray())
    embed1.add_field(name = member, value = f"- {member.name} was successfully banned from this server")
    embed1.add_field(name = "Reason", value = f"{reason}", inline = False)
    embed1.set_thumbnail(url =  ctx.guild.icon_url)
    #embed for user
    embed2 = discord.Embed(title = 'Banned', description = f"You were banned from {ctx.guild.name}", color = discord.Color.darker_gray())
    embed2.add_field(name = "Reason", value = f"{reason}", inline = False)
    embed2.set_thumbnail(url =  ctx.guild.icon_url)
    
    await member.send(embed = embed2)
    await member.ban(reason = reason)
    await ctx.send(embed = embed1)
  @ban.error
  async def ban_error(self, ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument): 
        await ctx.send("Please specify a **valid** user!")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("You need the **ban members** permission")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Please specify a **valid** user!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument): 
        await ctx.send("Please specify a **valid** user!")
    else:
        raise error


  #unban command: unbans someone who is Banned
  @commands.command(aliases = ["ub"], description="unbans a user from the server.")
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
      user = ban_entry.user

      if (user.name, user.discriminator) == (member_name, member_discriminator):
        #embed for server
        embed1 = discord.Embed(title = 'Unbanned', description = f"A user was Unbanned from this server", color = discord.Color.greyple())
        embed1.add_field(name = member, value = f"- {member} was successfully unbanned from this server")
        embed1.set_thumbnail(url =  ctx.guild.icon_url)
        await ctx.guild.unban(user)
        await ctx.send(embed = embed1)
        
        return

  #clear command: clears channel messages
  @commands.command(aliases = ["cl"], description = "clears a number of messages from the channel.\n\n\t- it deletes `<number of messages>` and the command message automatically, so don't be alarmed if the success message says it deleted one too many messages\n\t- if you dont supply any number, the bot will just delete your command message")
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, *, amount = 0):
    amount = amount
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"{amount+1} message(s）were cleared")
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=1)
  @clear.error
  async def clear_error(self, error, ctx):
    if isinstance(error, discord.ext.commands.errors.BadArgument): 
        await ctx.send("Please specify a **valid** number!")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions): 
        await ctx.send("You do not have the **manage messages** permission")
    else:
        raise error

def setup(client):
  client.add_cog(Moderation(client))
  print("mod is online")

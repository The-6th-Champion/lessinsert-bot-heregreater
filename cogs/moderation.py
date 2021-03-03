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
        await ctx.send("Please specify a **valid** user and a **required** reason!")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("You need the **kick members** permission")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Please specify a **valid** user!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument): 
        await ctx.send("Please specify a **valid** user!")
    else:
        raise error

#bellow is the old ban command
"""
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
        await ctx.send("Please specify a **valid** user and a **required** reason!")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("You need the **ban members** permission")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Please specify a **valid** user!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument): 
        await ctx.send("Please specify a **valid** user!")
    else:
        raise error"""
  @commands.command(aliases = ['b', 'forceban', 'fb'], description = 'Bans a user from the server. This user doesn\'t have to be a member of the server to be banned')
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, user, *, reason):

    user = user.replace("<", "")
    user = user.replace(">", "")
    user = user.replace("@", "")
    user = user.replace("!", "")
    user_id = int(user)

    #embed for server
    banneduser = await self.client.fetch_user(user_id)
    embed1 = discord.Embed(title = 'Banned :hammer:', description = "A user was banned from this server", color = discord.Color.darker_gray())
    embed1.add_field(name = banneduser, value = f"- {banneduser.name} was successfully banned from this server")
    embed1.add_field(name = "Reason", value = f"{reason}", inline = False)
    embed1.set_thumbnail(url =  ctx.guild.icon_url)
    #embed for user
    embed2 = discord.Embed(title = 'Banned', description = f"You were banned from {ctx.guild.name}", color = discord.Color.darker_gray())
    embed2.add_field(name = "Reason", value = f"{reason}", inline = False)
    embed2.set_thumbnail(url =  ctx.guild.icon_url)
    
    await ctx.guild.ban(banneduser, reason = reason)
    await banneduser.send(embed = embed2)
    await ctx.send(embed = embed1)
  @ban.error
  async def ban_error(self, ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument): 
        await ctx.send("Please specify a **valid** user! and **required** reason")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("You need the **ban members** permission")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Please specify a **valid** user!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument): 
        await ctx.send("Please specify a **valid** user! and **required** reason")
    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError): 
        await ctx.send("Something went wrong. check my permissions.")
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
  @unban.error
  async def unban_error(self, ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument): 
        await ctx.send("Please specify a **valid** user!")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("You need the **ban members** permission")
    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("Please specify a **valid** user!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument): 
        await ctx.send("Please specify a **valid** user!")
    else:
        raise error

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
  
  #mute command
  @commands.command(description = "Adds the role 'Muted - IBH' to the bot. The role will be made if it isn' already.")
  @commands.has_permissions(kick_members = True)
  async def mute(self, ctx, member : discord.Member, duration, *, reason):
    muted_role=discord.utils.get(ctx.guild.roles, name="Muted - IBH")
    if muted_role ==None:
      muted_role = await ctx.guild.create_role(name = "Muted - IBH")
    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
    tempmute= int(duration[0]) * time_convert[duration[-1]]
    #embed for server
    embed1 = discord.Embed(title = 'Muted :no_mouth:', description = f"A user was muted on this server", color = discord.Color.greyple())
    embed1.add_field(name = member, value = f"- {member} was successfully muted for {duration} this server.\n Reason: {reason}")
    embed1.set_thumbnail(url =  ctx.guild.icon_url)
    #embed for user
    embed2 = discord.Embed(title = 'Muted', description = f"You were muted on {ctx.guild.name} for {duration}", color = discord.Color.light_gray())
    embed2.add_field(name = "Reason", value = f"{reason}", inline = False)
    embed2.set_thumbnail(url = ctx.guild.icon_url)
    await member.add_roles(muted_role)
    await ctx.send(embed = embed1)
    await member.send(embed=embed2)
    await asyncio.sleep(tempmute)
    await member.remove_roles(muted_role)
  @mute.error
  async def mute_error(error, ctx):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
      await ctx.send("You do not have the *Kick members* permission")
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
      await ctx.send("Please specify a valid user, duration, and reason. duration must be a number followed by s, m, h, or d. ex) 5d OR 3h OR 22m OR 1s ")
    if isinstance(error, discord.ext.commands.errors.BadArgument):
      await ctx.send("Please make sure you have valid arguments. duration must be a number followed by s, m, h, or d. ex) 5d OR 3h OR 22m OR 1s ")
  

def setup(client):
  client.add_cog(Moderation(client))
  print("mod is online")

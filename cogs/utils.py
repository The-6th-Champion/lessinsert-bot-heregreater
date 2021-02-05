import discord
from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    #user info command: gives user info of a user
    @commands.command(aliases=["ui"])
    async def userinfo(self, ctx, member: discord.Member = None):
        pronounthing = "This user"
        if member == None:
            member = ctx.author
            pronounthing = "You"
        if member.bot == False:
            botcon = "No"
        else:
            botcon = "Yes"

        embed = discord.Embed(
            title='Userinfo',
            description=f"Here is some Information on {member.name}",
            color=discord.Color.blue())

        embed.add_field(
            name=member,
            value=
            f"- User's name: {member.name}\n- User's ID: {member.id}\n- User's Discriminator: {member.discriminator}\n- User is a Bot: {botcon}"
        )
        joindate=member.joined_at.strftime("%c %Z")
        createdate=member.created_at.strftime("%c %Z")
        embed.add_field(
            name="Dates",
            value=
            f"{pronounthing} **joined this server** on {joindate}\n{pronounthing} **joined discord** on {createdate}"
        )

        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)
    

    #serverinfo command: gives server info
    @commands.command(aliases=["si"])
    async def serverinfo(self, ctx):
        createdate=ctx.guild.created_at.strftime("%c %Z")
        em = discord.Embed(title = f"Info about {ctx.guild.name}", description = f"This server's ID is {ctx.guild.id}", color = discord.Color.gold())
        em.add_field(name="Owner", value=f"{ctx.guild.owner.mention}")
        em.add_field(name="Member Count", value=f"{ctx.guild.member_count}", inline = True)
        em.add_field(name="Boosting", value=f"{ctx.guild.premium_subscribers}\n{ctx.guild.premium_subscription_count}", inline = True)
        em.add_field(name="Created On", value=f"{createdate}", inline = False)
        em.add_field(name="Channels", value=f"Text: {len(ctx.guild.text_channels)}\nVoice:{len(ctx.guild.voice_channels)}\nCategories:{len(ctx.guild.categories)}", inline = True)
        em.add_field(name="Emojis", value=f"{ctx.guild.emojis}", inline = False)
        em.set_thumbnail(url = f"{ctx.guild.icon_url}")
        em.set_footer(text=f"Requested By {ctx.author.mention}", icon_url=f"{ctx.author.default_avatar_url}")
        await ctx.send(embed=em)
        
 
    #invite command. gives bot invite and invite to <ISH>
    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title='Invites',
            description=
            f"Use the provided links for inviting the bot to your server, or to go to the supprot server for <Insert Bot Here>",
            color=discord.Color.blue())

        embed.add_field(
            name="Bot Inviting Link:",
            value=
            "https://discord.com/api/oauth2/authorize?client_id=780928781858373672&permissions=8&scope=bot"
        )
        embed.add_field(
            name="Support Server Invite Link:",
            value="<Insert Server Here>\nhttps://discord.gg/685TrVGQyd",
            inline=False)
        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/icons/764927590070353940/50b03d8a37801c444dd8da8d7a2cc18b.webp?size=1024"
        )
        await ctx.send(embed=embed)

    #prefix command. gives bot prefix
    @commands.command()
    async def prefix(self, ctx):
        embed = discord.Embed(
            title='Prefix',
            description=f"This Bot's prefix is `>>`",
            color=discord.Color.blue())
        await ctx.send(embed=embed)

    #status
    @commands.command()
    async def status(self, ctx):
        embed = discord.Embed(
            title='Status',
            description="The bot is online, Obviously :sunglasses: :)",
            color=discord.Color(0x40AC7B))
        embed.add_field(name = "Server Count", value = len(self.client.guilds))
        await ctx.send(embed=embed)

    #role info command: gives role id of a role
    @commands.command(aliases=["ri"])
    async def roleinfo(self, ctx, role: discord.Role):
        await ctx.send(f'Role ID: {role.id}')

    #upvote command: duh
    @commands.command(aliases=["vote"])
    async def upvote(self, ctx):
        em = discord.Embed(
            title="Upvote This Bot!!!",
            description="Vote at https://top.gg/bot/780928781858373672/vote",
            color=discord.Color(0xf0f))
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Utils(client))
    print("util is online")

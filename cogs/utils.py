import discord
from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    #user info command: gives user id of a user
    @commands.command(aliases=["ui"])
    async def userinfo(self, ctx, user: discord.User = None):
        if user is None:
            await ctx.send("Please provide a user to send info on!")
            return
        if user.bot == False:
            botcon = "No"
        else:
            botcon = "Yes"

        embed = discord.Embed(
            title='Userinfo',
            description=f"Here is some Information on {user.name}",
            color=discord.Color.blue())

        embed.add_field(
            name=user,
            value=
            f"- User's name: {user.name}\n- User's ID: {user.id}\n- User's Discriminator: {user.discriminator}\n- User is a Bot: {botcon}"
        )

        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

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

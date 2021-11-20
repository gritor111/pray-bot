from discord.ext import commands
import datetime
import discord


class Activity(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def daily(self, ctx, *, member: discord.Member = None):
        user = ctx.author

        if member:
            user = member

        daily_pray_count = len(await self.bot.hdb.get_daily_count(user))

        embed = discord.Embed(title=f"{user.name}'s daily pray count: {daily_pray_count}", color=discord.Color.green())

        await ctx.channel.send(embed=embed)

    @commands.command(name="active", aliases=["weekly", "week"])
    async def weekly(self, ctx, *, member: discord.Member = None):
        user = ctx.author

        if member:
            user = member

        print(user)

        weekly_pray_count = len(await self.bot.hdb.get_count_by_time(user, '1 week'))

        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=user.name, icon_url=str(user.avatar_url))

        if weekly_pray_count >= 200:
            embed.description = f"**{user.name}** has prayed to louis **{weekly_pray_count} times in the last week"

        await ctx.channel.send(embed=embed)

    @commands.command()
    async def monthly(self, ctx, *, member: discord.Member = None):
        user = ctx.author

        if member:
            user = member

        daily_pray_count = len(await self.bot.hdb.get_count_by_time(user, '1 month'))

        embed = discord.Embed(title=f"{user.name}'s monthly pray count: {daily_pray_count}",
                              color=discord.Color.green())

        await ctx.channel.send(embed=embed)

    @commands.command(name="alltime", aliases=["at"])
    async def alltime(self, ctx, *, member: discord.Member = None):
        user = ctx.author

        if member:
            user = member

        alltime_prays = (await self.bot.hdb.get_user(user.id))["pray_count"]

        embed = discord.Embed(title=f"{user.name}'s All Time pray count: {alltime_prays}", color=discord.Color.green())

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Activity(bot))

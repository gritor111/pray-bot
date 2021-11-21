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

        weekly_pray_count = len(await self.bot.hdb.get_count_by_time(user, '1 week'))

        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=user, icon_url=str(user.avatar_url))
        embed.description = f"**{user.name}** has prayed to louis **{weekly_pray_count}** times in the last week"

        if weekly_pray_count < 200:
            progress_bar_full_1 = "<a:Bar1Full:909895429540421672>"
            progress_bar_full_2 = "<a:Bar2Full:909895429322313850>"
            progress_bar_empty_1 = "<:Bar1Empty:909897948698128395>"
            progress_bar_empty_2 = "<:Bar2Empty:909895429217460265>"
            progress_bar_empty_3 = "<:Bar3Empty:909895429540429844>"

            progress = ("■" * int((weekly_pray_count / 300) * 10)).ljust(10, "□")

            #  i made this logic at like 1am dont judge me

            if "■" in progress:
                progress = list(progress)
                progress[0] = progress_bar_full_1
                progress = ''.join(progress)

            else:
                progress = list(progress)
                progress[0] = progress_bar_empty_1  # replace first char
                progress = ''.join(progress)

            progress = list(progress)
            progress[-1] = progress_bar_empty_3  # replace last char
            progress = ''.join(progress)

            progress = progress.replace("■", progress_bar_full_2)
            progress = progress.replace("□", progress_bar_empty_2)

            embed.description += f"\n{user.name} needs to pray __{300 - weekly_pray_count}__" \
                                 f" more times to louis to get the <@&911639659430432838> role\n{progress}"

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

    @commands.command(name="count", aliases=["c"])
    async def count(self, ctx, *, member: discord.Member = None):
        user = ctx.author

        if member:
            user = member

        prays = len(await self.bot.hdb.get_count_by_time(user, "1 day"))

        embed = discord.Embed(title=f"{user.name}'s count: {prays}", color=discord.Color.green())

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Activity(bot))

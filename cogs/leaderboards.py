from discord.ext import commands
import discord
import itertools


class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_top_body_time(self, author, pray_logs, limit):

        body = ''

        sorted_users = {}

        for pray in pray_logs:

            if pray['username'] not in sorted_users:
                sorted_users[pray['username']] = 1
                continue

            sorted_users[pray['username']] += 1

        sorted_users = dict(sorted(sorted_users.items(), key=lambda user: user[1], reverse=True))  # sort by pray_count

        for i, user in enumerate(dict(itertools.islice(sorted_users.items(), limit))):
            body += f'\n\n`#{i + 1}` {user} - **{sorted_users[user]}**'

        if author.name not in dict(itertools.islice(sorted_users.items(), limit)):
            if author.name not in sorted_users:
                sorted_users[author.name] = 0

            body += f"\n**⋮**\n`#{list(sorted_users.keys()).index(author.name) + 1}` {author.name} - **{sorted_users[author.name]}**"

        return body

    @commands.group(name='top', aliases=['t'])
    async def top(self, ctx):

        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=discord.Color.blue(), title='Leaderboards and stuff')

            embed.add_field(name='DAILY', value=f"`{ctx.prefix}top daily`\n", inline=False)
            embed.add_field(name='WEEKLY', value=f"`{ctx.prefix}top weekly`\n", inline=False)
            embed.add_field(name='ALLTIME', value=f"`{ctx.prefix}top alltime`")

            await ctx.channel.send(embed=embed)

    @top.command(name='daily', aliases=['d'])
    async def top_daily(self, ctx, limit=5):

        daily_pray_logs = await self.bot.hdb.get_daily_lb_users()
        embed = discord.Embed(color=discord.Color.blue())

        body = await self.get_top_body_time(ctx.author, daily_pray_logs, limit)

        embed.add_field(name='🙏 Daily pray leaderboard 🙏', value=body)

        await ctx.channel.send(embed=embed)

    @top.command(name='weekly', aliases=['w'])
    async def top_weekly(self, ctx, limit=5):

        weekly_pray_logs = await self.bot.hdb.get_weekly_lb_users()

        embed = discord.Embed(color=discord.Color.blue())

        body = await self.get_top_body_time(ctx.author, weekly_pray_logs, limit)

        embed.add_field(name='🙏 Weekly pray leaderboard 🙏', value=body)

        await ctx.channel.send(embed=embed)

    @top.command(name='alltime', aliases=['at'])
    async def all_time(self, ctx, limit=5):

        pray_logs = await self.bot.hdb.get_pray_logs()

        embed = discord.Embed(color=discord.Color.blue())

        body = await self.get_top_body_time(ctx.author, pray_logs, limit)

        embed.add_field(name='🙏 All time pray leaderboard 🙏', value=body)

        await ctx.channel.send(embed=embed)

    @top.command(name="level", aliases=["xp"])
    async def top_xp(self, ctx, limit=5):

        level_leaderboard = await self.bot.hdb.get_users()

        level_group = []
        new_level_leaderboard = []

        for i, user in enumerate(level_leaderboard):
            user_lvl = user["level"]
            if user_lvl != level_leaderboard[i - 1]["level"]:
                level_group = sorted(level_group, key=lambda user_info: user_info["xp"], reverse=True)
                new_level_leaderboard += level_group
                level_group.clear()

            level_group.append(user)

        print(new_level_leaderboard)



def setup(bot):
    bot.add_cog(Leaderboard(bot))

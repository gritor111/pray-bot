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

            if pray['user_id']:  # check theres id
                if pray['user_id'] not in sorted_users:
                    sorted_users[pray['user_id']] = 1
                    continue

                sorted_users[pray['user_id']] += 1
        print(sorted_users)
        sorted_users = dict(sorted(sorted_users.items(), key=lambda user: user[1], reverse=True))  # sort by pray_count
        print(sorted_users)
        for i, user_id in enumerate(dict(itertools.islice(sorted_users.items(), limit))):
            print(user_id)
            member = await self.bot.fetch_user(user_id)
            body += f'\n\n`#{i + 1}` {member.name} - **{sorted_users[user_id]}**'

        if author.id not in dict(itertools.islice(sorted_users.items(), limit)):
            if author.id not in sorted_users:
                sorted_users[author.id] = 0

            body += f"\n**⋮**\n`#{list(sorted_users.keys()).index(author.id) + 1}` {author.name} - **{sorted_users[author.id]}**"

        return body

    @commands.group(name='top', aliases=['t'])
    async def top(self, ctx):

        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=discord.Color.blue(), title='Leaderboards and stuff')

            embed.add_field(name='DAILY', value=f"`{ctx.prefix}top daily`\n", inline=False)
            embed.add_field(name='WEEKLY', value=f"`{ctx.prefix}top weekly`\n", inline=False)
            embed.add_field(name='ALLTIME', value=f"`{ctx.prefix}top alltime`", inline=False)
            embed.add_field(name='LEVELS', value=f"`{ctx.prefix}top level`\n", inline=False)

            await ctx.channel.send(embed=embed)

    @top.command(name='daily', aliases=['d'])
    async def top_daily(self, ctx, limit=5):

        daily_pray_logs = await self.bot.hdb.get_daily_lb_users()

        body = await self.get_top_body_time(ctx.author, daily_pray_logs, limit)

        embed = discord.Embed(color=discord.Color.blue(), description=body)

        embed.set_author(name="Daily Leaderboard", icon_url=str(ctx.author.avatar_url))

        await ctx.channel.send(embed=embed)

    @top.command(name='weekly', aliases=['w'])
    async def top_weekly(self, ctx, limit=5):

        weekly_pray_logs = await self.bot.hdb.get_weekly_lb_users()

        body = await self.get_top_body_time(ctx.author, weekly_pray_logs, limit)

        embed = discord.Embed(color=discord.Color.blue(), description=body)

        embed.set_author(name="Weekly Leaderboard", icon_url=str(ctx.author.avatar_url))

        await ctx.channel.send(embed=embed)

    @top.command(name='alltime', aliases=['at'])
    async def all_time(self, ctx, limit=5):

        pray_logs = await self.bot.hdb.get_pray_logs()

        body = await self.get_top_body_time(ctx.author, pray_logs, limit)

        embed = discord.Embed(color=discord.Color.blue(), description=body)

        embed.set_author(name="All Time Leaderboard", icon_url=str(ctx.author.avatar_url))

        await ctx.channel.send(embed=embed)

    @top.command(name="level", aliases=["xp"])
    async def top_xp(self, ctx, limit=5):

        level_leaderboard = await self.bot.hdb.get_level_leaderboard()

        level_group = []
        new_level_leaderboard = []

        for i, user in enumerate(level_leaderboard):
            user_lvl = user["level"]

            if user_lvl != level_leaderboard[i - 1]["level"]:
                level_group = sorted(level_group, key=lambda user_info: user_info["current_xp"], reverse=True)
                new_level_leaderboard.extend(level_group)
                level_group = []

            level_group.append(user)

        body = ''

        for i, user in enumerate(new_level_leaderboard[:limit]):
            body += f'\n\n`#{i + 1}` {user["username"]} - **level {user["level"]} {user["current_xp"]}xp**'

        embed = discord.Embed(color=discord.Color.blue(), description=body)
        embed.set_author(name="Levels Leaderboard", icon_url=str(ctx.author.avatar_url))

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Leaderboard(bot))

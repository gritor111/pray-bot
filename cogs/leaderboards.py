from discord.ext import commands
import discord
import itertools

class Leaderboard(commands.Cog):

  def __init__(self, bot):
      self.bot = bot

  async def get_top_body(self, pray_logs, limit):

    body = ''

    sorted_users = {}

    for pray in pray_logs:

      if pray['username'] not in sorted_users:
        sorted_users[pray['username']] = 1
        continue
      
      sorted_users[pray['username']] += 1
    
    sorted_users = sorted(sorted_users.items(), key=lambda user: user[1], reverse=True)  # sort by pray_count

    sorted_users = sorted_users[:limit]  # slice the list
    print(sorted_users)
    for i, (username, pray_count) in enumerate(sorted_users):

      body += f'\n\n`#{i + 1}` {username} - **{pray_count}**'

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

    body = await self.get_top_body(ctx.author, daily_pray_logs, limit)

    embed.add_field(name='🙏 Daily pray leaderboard 🙏', value=body)


    await ctx.channel.send(embed=embed)

  @top.command(name='weekly', aliases=['w'])
  async def top_weekly(self, ctx, limit=5):

    weekly_pray_logs = await self.bot.hdb.get_lb_users_by_time('week')

    embed = discord.Embed(color=discord.Color.blue())

    body = await self.get_top_body(weekly_pray_logs, limit)

    embed.add_field(name='🙏 Weekly pray leaderboard 🙏', value=body)


    await ctx.channel.send(embed=embed)

  @top.command(name='alltime', aliases=['at'])
  async def all_time(self, ctx, limit=5):

    pray_logs = await self.bot.hdb.get_pray_logs()

    embed = discord.Embed(color=discord.Color.blue())

    body = await self.get_top_body(pray_logs, limit)

    embed.add_field(name='🙏 All time pray leaderboard 🙏', value=body)

    await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Leaderboard(bot))

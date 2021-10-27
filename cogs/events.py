from discord.ext import commands
import discord

class Events(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx, e):
    pass

  @commands.Cog.listener()
  async def on_message(self, ctx):

    if ctx.author.id == 408785106942164992:  # checks if its a message from owo bot
      
      if ctx.content.startswith('**🙏 |'):  # checks if its a pray message

        if ctx.content.split('**')[3] == '!Louis':

          prayer_username = ctx.content.split('**')[1].split('🙏 | ')[1]
          user = await self.bot.hdb.get_user(prayer_username)

          if user == []:  # not in db
            await self.bot.hdb.add_user(prayer_username)

          await self.bot.hdb.add_pray(prayer_username)

def setup(bot):
  bot.add_cog(Events(bot))
from discord.ext import commands
import discord
import datetime

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):

        if ctx.author.id == 408785106942164992:  # checks if its a message from owo bot

            if ctx.content.startswith('**🙏 |'):  # checks if its a pray message

                if ctx.content.split('**')[3] == '!Louis':

                    prayer_username = ctx.content.split('**')[1].split('🙏 | ')[1]
                    user = await self.bot.hdb.get_user(prayer_username)

                    if not user:  # not in db
                        await self.bot.hdb.add_user(prayer_username)

                    last_pray_timestamp = await self.bot.hdb.get_last_pray_user(prayer_username)["timestamp"]
                    print((last_pray_timestamp - datetime.datetime.utcnow()) >= datetime.time(minute=5), (last_pray_timestamp - datetime.datetime.utcnow()), datetime.time(minute=5))
                    if last_pray_timestamp:  # checking if user prayed before
                        if (last_pray_timestamp - datetime.datetime.utcnow()) >= datetime.time(minute=5):
                            await self.bot.hdb.add_pray(prayer_username)


def setup(bot):
    bot.add_cog(Events(bot))

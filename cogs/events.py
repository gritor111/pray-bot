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
                    user = await self.bot.hdb.get_user('username', prayer_username)

                    if not user:  # not in db
                        await self.bot.hdb.add_user(prayer_username)

                    last_pray = await self.bot.hdb.get_last_pray_user(prayer_username)

                    if last_pray:  # checking if user prayed before
                        if (datetime.datetime.now(datetime.timezone.utc) - last_pray[0]["timestamp"])\
                                >= datetime.timedelta(minutes=2):
                            await self.bot.hdb.add_pray(prayer_username)

                    else:  # first ever pray
                        await self.bot.hdb.add_pray(prayer_username)

                    await ctx.add_reaction("🙏")

    @commands.Cog.listener()
    async def on_command(self, ctx):  # add user to database
        user = await self.bot.hdb.get_user('user_id', ctx.author.id)
        print(user)
        if not user:
            await self.bot.hdb.add_user(user_id=ctx.author.id)

        if not user[0]["user_id"]:
            await self.bot.hdb.update_user('user_id', ctx.author.id, ctx.author.name)


def setup(bot):
    bot.add_cog(Events(bot))

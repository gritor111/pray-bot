from discord.ext import commands
import datetime
import random
import math


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.XP_MULTI = 5

    @commands.Cog.listener()
    async def on_message(self, ctx):

        if ctx.author.id == 408785106942164992:  # checks if its a message from owo bot

            if ctx.content.startswith('**🙏 |'):  # checks if its a pray message

                if ctx.content.split('**')[3] == '!Louis':

                    prayer_username = ctx.content.split('**')[1].split('🙏 | ')[1]
                    user = await self.bot.hdb.get_user(prayer_username)

                    if not user:  # not in db
                        await self.bot.hdb.add_user(username=prayer_username)

                    last_pray = await self.bot.hdb.get_last_pray_user(prayer_username)

                    if not last_pray:  # checking if its the user first pray
                        await self.bot.hdb.add_pray(prayer_username)
                        await ctx.add_reaction("🙏")
                        return  # no xp hehehhe

                    if (datetime.datetime.now(datetime.timezone.utc) - last_pray[0]["timestamp"])\
                            >= datetime.timedelta(minutes=2):

                        await self.bot.hdb.add_pray(prayer_username, user[0]["user_id"])
                        await ctx.add_reaction("🙏")

                        xp = random.randint(10, 16) * 5
                        user_lvl = user[0]["level"]
                        user_xp = user[0]["current_xp"] + xp
                        level_up = self.check_level_up(user_xp, user_lvl)

                        if level_up:
                            await self.distribute_rewards(user[0]["id"] if user[0]["id"] else user[0]["username"], user_lvl + 1)  # if id exists use it cus more secure and stuff
                            await self.bot.hdb.set_user_xp(user[0]["id"] if user[0]["id"] else user[0]["username"], 0)  # reset xp

                        await self.bot.hdb.set_user_xp(user[0]["id"] if user[0]["id"] else user[0]["username"], user_xp)  # give xp
                        user = await self.bot.hdb.get_user(prayer_username)
                        print(user[0]["current_xp"])

    @commands.Cog.listener()
    async def on_command(self, ctx):  # add user to database
        user = await self.bot.hdb.get_user(ctx.author.name)

        if not user:
            await self.bot.hdb.add_user(user_id=ctx.author.id)

        if not user[0]["user_id"]:
            await self.bot.hdb.update_user(ctx.author.id, ctx.author.name)

    def check_level_up(self, user_xp, level):
        required_xp = 5000 + math.pow(level*self.XP_MULTI, 2)

        if user_xp >= required_xp:
            return True

        return False

    async def distribute_rewards(self, user, user_lvl):
        louis_dm = self.bot.get_channel(289411794672418819)
        await louis_dm.send(f"`owogive {user} {user_lvl*25000}`\n {user} levelled up to level {user_lvl}")




def setup(bot):
    bot.add_cog(Events(bot))

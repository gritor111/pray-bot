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
                        await ctx.add_reaction("<:prayge:910989570299002900>")
                        return  # no xp hehehhe

                    if (datetime.datetime.now(datetime.timezone.utc) - last_pray[0]["timestamp"])\
                            >= datetime.timedelta(minutes=2):

                        await self.bot.hdb.add_pray(prayer_username, user[0]["user_id"])
                        await ctx.add_reaction("<:prayge:910989570299002900>")

                        xp = random.randint(10, 16) * 5
                        user_lvl = user[0]["level"]
                        user_xp = user[0]["current_xp"] + xp
                        level_up = self.bot.util.check_level_up(user_xp, user_lvl)
                        user_id_username = user[0]["user_id"] if user[0]["user_id"] else user[0]["username"]

                        if level_up:
                            await self.bot.util.distribute_rewards(user_id_username, user_lvl + 1)  # if id exists use it cus more secure and stuff
                            await self.bot.hdb.set_user_level(user_id_username, user_lvl + 1)
                            await self.bot.hdb.set_user_xp(user_id_username, 0)  # reset xp
                            await ctx.channel.send(f"{user[0]['username']} levelled up to level {user_lvl + 1}")
                            return

                        await self.bot.hdb.set_user_xp(user[0]["user_id"] if user[0]["user_id"] else user[0]["username"], user_xp)  # give xp

    @commands.Cog.listener()
    async def on_command(self, ctx):  # add user to database
        user = await self.bot.hdb.get_user(ctx.author.name)

        if not user:
            await self.bot.hdb.add_user(user_id=ctx.author.id, username=ctx.author.name)

        if not user[0]["user_id"]:
            await self.bot.hdb.update_user_id(ctx.author.id, ctx.author.name)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        print(before.name, after.name)
        if before.name != after.name:  # user has changed username
            user = await self.bot.hdb.get_user(before.name)
            if user and user[0]["user_id"] == after.id:
                await self.bot.hdb.update_user_username(after.name, before.name)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"added {member.name} to the database")
        await self.bot.hdb.add_user(username=member.name, user_id=member.id)


def setup(bot):
    bot.add_cog(Events(bot))

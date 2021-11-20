from discord.ext import commands, tasks
import datetime
import random
import math


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.XP_MULTI = 5

        self.update_active.start()

    @commands.Cog.listener()
    async def on_message(self, ctx):

        if ctx.author.id == 408785106942164992:  # checks if its a message from owo bot

            if ctx.content.startswith('**🙏 |'):  # checks if its a pray message

                if ctx.content.split('**')[3] == '!Louis':

                    prayer_username = ctx.content.split('**')[1].split('🙏 | ')[1]
                    members = ctx.guild.members
                    members_with_username = []
                    member = 0  # just so i can use it later on

                    for member in members:
                        if member.name == prayer_username:
                            members_with_username.append(member)

                    if len(members_with_username) <= 1:  # no users with the same username
                        member = members_with_username[0]
                        user = await self.bot.hdb.get_user(member.id)

                    else:  # users with the same username ;-;
                        async for message in ctx.channel.history(10):
                            if message.author.name == prayer_username:
                                member = message.author
                                user = await self.bot.hdb.get_user(member.id)

                    last_pray = await self.bot.hdb.get_last_pray_user(user["user_id"])

                    if not last_pray:  # checking if its the user first pray
                        await self.bot.hdb.add_pray(prayer_username, user["user_id"])
                        await ctx.add_reaction("<:prayge:910989570299002900>")
                        return  # no xp hehehhe

                    if (datetime.datetime.now(datetime.timezone.utc) - last_pray[0]["timestamp"])\
                            >= datetime.timedelta(minutes=2):

                        await self.bot.hdb.add_pray(prayer_username, user["user_id"])
                        await ctx.add_reaction("<:prayge:910989570299002900>")

                        # handle xp

                        rand_xp_multi = 3

                        if datetime.datetime.today().weekday() > 4:  # weekend
                            rand_xp_multi = 5

                        xp = random.randint(10, 16) * rand_xp_multi
                        user_lvl = user["level"]
                        user_xp = user["current_xp"] + xp
                        user_id = user["user_id"]
                        level_up = self.bot.util.check_level_up(user_xp, user_lvl)

                        if level_up:
                            await self.bot.util.distribute_rewards(user_id, user_lvl + 1)  # if id exists use it cus more secure and stuff
                            await self.bot.hdb.set_user_level(user_id, user_lvl + 1)
                            await self.bot.hdb.set_user_xp(user_id, 0)  # reset xp
                            await ctx.channel.send(f"{user['username']} levelled up to level {user_lvl + 1}")
                            return

                        await self.bot.hdb.set_user_xp(user_id, user_xp)  # give xp

                        # handle active

                        weekly_pray_count = len(await self.bot.hdb.get_count_by_time(member, "week"))
                        active_role = ctx.guild.get_role(911639659430432838)
                        if weekly_pray_count == 200:
                            await member.add_roles(active_role)
                            await ctx.channel.send(f"send help i need a good message for this also {member} got <@&911639659430432838>")

                        elif weekly_pray_count < 200 and active_role in member.roles:
                            await member.remove_roles(active_role)

    @commands.Cog.listener()
    async def on_command(self, ctx):  # add user to database
        user = await self.bot.hdb.get_user(ctx.author.id)

        if not user:
            await self.bot.hdb.add_user(user_id=ctx.author.id, username=ctx.author.name)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:  # user has changed username
            user = await self.bot.hdb.get_user(before.id)
            if user:
                await self.bot.hdb.update_user_username(after.name, before.name)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        user = await self.bot.hdb.get_user(member.id)
        if not user:
            await self.bot.hdb.add_user(username=member.name, user_id=member.id)
        # else:
        #     await self.bot.hdb.update_user_id(member.id, member.name)
        # TODO add support for user who left and rejoined

    @tasks.loop(minutes=5)
    async def update_active(self):
        guild = await self.bot.fetch_guild(888467716732747827)
        active_role = guild.get_role(911639659430432838)
        print(dir(guild))
        members = guild.fetch_members()
        print(members)
        for member in members:
            print(13)
            if member.bot:
                continue

            weekly_pray_count = len(await self.bot.hdb.get_count_by_time(member, "week"))
            print(member, weekly_pray_count)
            if weekly_pray_count < 200 and (active_role in member.roles):
                print(1)
                await member.remove_roles(active_role)

            elif weekly_pray_count >= 200 and (active_role not in member.roles):
                print(2)
                await member.add_roles(active_role)


def setup(bot):
    bot.add_cog(Events(bot))

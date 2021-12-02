from discord.ext import commands
import datetime


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fixpraydupes")
    @commands.is_owner()
    async def fix_pray_dupes(self, ctx):
        users = list(set(await self.bot.db.fetch("""SELECT username FROM users""")))
        text = ''

        for user in users:
            user = user["username"]
            user_logs = await self.bot.db.fetch(
                """SELECT * FROM pray_logs WHERE username = $1 ORDER BY timestamp DESC""", user)

            prev_pray_timestamp = None
            dupes = []
            for pray in user_logs:
                if prev_pray_timestamp:
                    diff = prev_pray_timestamp - pray["timestamp"]

                    if diff < datetime.timedelta(minutes=2):  # not 5 because theres lag
                        dupes.append(pray["timestamp"])

                prev_pray_timestamp = pray["timestamp"]

            for timestamp in dupes:
                print(timestamp)
                # await self.bot.db.execute("""DELETE FROM pray_logs WHERE username = $1 AND timestamp = $2""", user,
                #                           timestamp)

            if len(dupes) > 0:
                text += f"removed {len(dupes)} from {user} \n"

        print(text)

    @commands.command(name="fixuserdupes")
    @commands.is_owner()
    async def fix_user_dupes(self, ctx):
        users = await self.bot.db.fetch("""SELECT * FROM users""")
        users_no_dupes = list(set(await self.bot.db.fetch("""SELECT * FROM users""")))

        for user in users_no_dupes:

            user_sublist = []
            for user_dupe in users:
                if user_dupe["username"] == user["username"]:
                    user_sublist.append(user_dupe)

            print(user_sublist)
            highest_level = sorted(user_sublist, key=lambda user_row: user_row["level"], reverse=True)[0]["level"]
            xp = sorted(user_sublist, key=lambda user_row: user_row["level"], reverse=True)[0]["current_xp"]

            user_id = user["user_id"]
            pray_count = (await self.bot.db.fetch("""SELECT COUNT(*) FROM pray_logs WHERE user_id = $1""", user_id))[0]
            await self.bot.db.execute("""DELETE FROM users WHERE username = $1""", user["username"])

            await self.bot.hdb.add_user(username=user["username"], pray_count=pray_count, xp=xp, level=highest_level)

        await ctx.channel.send("done")

    @commands.command(name='fixuserids')
    @commands.is_owner()
    async def fix_user_ids(self, ctx):
        members = ctx.guild.members
        for member in members:
            if member.bot:  # its a bot )<
                continue

            user = await self.bot.hdb.get_user_by_name(member.name)
            print(user)

            if not user:
                await self.bot.hdb.add_user(username=member.name, user_id=member.id)
                continue

            if user["user_id"]:  # already has id
                continue

            else:  # doesnt have id
                print(member)
                await self.bot.hdb.update_user_id(member.id, member.name)
                continue

        await ctx.channel.send("synced user ids")

    @commands.command("syncuserprays")
    @commands.is_owner()
    async def sync_user_prays(self):
        users = self.bot.db.fetch("""SELECT * FROM users""")
        for user in users:
            if user["user_id"]:
                print(user)
                pray_count = await self.bot.db.fetchrow("""SELECT COUNT(*) FROM pray_logs WHERE user_id = $1""", user["user_id"])
                await self.bot.db.execute("""UPDATE users SET pray_count = $1 WHERE user_id = $2""", pray_count, user["user_id"])


def setup(bot):
    bot.add_cog(Owner(bot))

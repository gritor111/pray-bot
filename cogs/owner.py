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

            highest_level = max(sorted(user_sublist, key=lambda user_row: user_row["level"], reverse=True))["level"]
            xp = max(sorted(user_sublist, key=lambda user_row: user_row["level"], reverse=True))["current_xp"]

            username = user["username"]
            pray_count = \
            (await self.bot.db.fetch("""SELECT COUNT(*) FROM pray_logs WHERE username = $1""", username))[0]["count"]
            await self.bot.db.execute("""DELETE FROM users WHERE username = $1""", username)

            await self.bot.hdb.add_user(username=username, pray_count=pray_count, xp=xp, level=highest_level)

        await ctx.channel.send("done")

    @commands.command(name='fixuserids')
    @commands.is_owner()
    async def fix_user_ids(self, ctx):
        members = ctx.guild.members
        for member in members:
            if member.bot:  # its a bot )<
                continue

            user = await self.bot.db.fetch("""SELECT * FROM users WHERE user_id = $1""", member.id)
            print(user)
            if user:  # already has id
                continue

            user = await self.bot.db.fetch("""SELECT * FROM users WHERE username = $1""", member.name)
            print(user)
            if user:  # doesnt have id
                await self.bot.hdb.update_user_id(member.id, member.name)
                continue

            print(user)
            # user isnt in database
            await self.bot.hdb.add_user(username=member.name, user_id=member.id)

        await ctx.channel.send("synced user ids")


def setup(bot):
    bot.add_cog(Owner(bot))

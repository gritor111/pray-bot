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
        users = list(set(await self.bot.db.fetch("""SELECT * FROM users""")))

        for user in users:
            username = user["username"]
            pray_count = \
            (await self.bot.db.fetch("""SELECT COUNT(*) FROM pray_logs WHERE username = $1""", username))[0]["count"]
            await self.bot.db.execute("""DELETE FROM users WHERE username = $1""", username)
            await self.bot.hdb.add_user(username=username, pray_count=pray_count)

        await ctx.channel.send("done")

    @commands.command(name='fixuserids')
    @commands.is_owner()
    async def fix_user_ids(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Owner(bot))

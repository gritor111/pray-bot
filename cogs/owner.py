from discord.ext import commands
import datetime


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fixpraydupes")
    @commands.is_owner()
    async def fix_pray_dupes(self, ctx):
        users = self.bot.db.fetch("""SELECT * FROM users""")
        for user in users:
            print(user)
            # user_logs = await self.bot.db.fetch("""SELECT * FROM pray_logs WHERE username = $1 ORDER BY timestamp DESC""", user)
            #
            # prev_pray_timestamp = None
            # dupes = []
            # for pray in user_logs:
            #     if prev_pray_timestamp:
            #         diff = prev_pray_timestamp - pray["timestamp"]
            #         if diff < datetime.timedelta(minutes=2):  # not 5 because theres lag
            #             dupes.append(pray["timestamp"])
            #     prev_pray_timestamp = pray["timestamp"]
            # for timestamp in dupes:
            #     print(timestamp)
            #     await self.bot.db.execute("""DELETE FROM pray_logs WHERE username = $1 AND timestamp = $2""", user, timestamp)
            # print(user, len(dupes))

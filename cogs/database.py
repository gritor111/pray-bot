from discord.ext import commands
import datetime


class Database(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_user(self, username):
        return await self.bot.db.fetch("SELECT * FROM users WHERE username=$1", username)

    async def add_user(self, username):
        await self.bot.db.execute("""INSERT INTO users (username) VALUES ($1)""", username)

    async def add_pray(self, username):
        await self.bot.db.execute("""INSERT INTO pray_logs (username, timestamp) VALUES ($1, $2)""", username,
                                  datetime.datetime.utcnow())

        await self.bot.db.execute("""UPDATE users SET pray_count = pray_count + 1 WHERE username = $1""",
                                  username)  # update count

    async def get_top_prays(self, limit):
        return await self.bot.db.fetch("""SELECT * FROM users ORDER BY pray_count DESC LIMIT $1""", limit)

    async def get_count_by_time(self, user, timetype):
        return await self.bot.db.fetch(
            """SELECT * FROM pray_logs WHERE timestamp > timestamp - ('1' || $1)::interval AND username = $2""",
            timetype, user.name)

    async def get_daily_count(self, user):
        return await self.bot.db.fetch(
            """SELECT * FROM pray_logs WHERE timestamp > CURRENT_DATE::timestamp AND username = $1""", user.name)

    async def get_daily_lb_users(self):
        return await self.bot.db.fetch("""SELECT * FROM pray_logs WHERE timestamp > CURRENT_DATE::timestamp""")

    async def get_lb_users_by_time(self, timetype):
        return await self.bot.db.fetch(
            """SELECT * FROM pray_logs WHERE timestamp > timestamp - ('1' || $1)::interval""", timetype)

    async def get_pray_logs(self):
        return await self.bot.db.fetch("""SELECT * FROM pray_logs""")

    async def get_weekly_lb_users(self):  # weekly
        return await self.bot.db.fetch(
            """SELECT * FROM pray_logs WHERE timestamp > DATE_TRUNC('week', NOW()) - '1 day'::interval""")

    async def get_last_pray_user(self, user):
        return await self.bot.db.fetch("""SELECT * FROM pray_logs WHERE user = $1 ORDER BY timestamp DESC LIMIT 1""",
                                          user)


def setup(bot):
    bot.add_cog(Database(bot))

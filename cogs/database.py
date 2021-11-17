from discord.ext import commands
import datetime


class Database(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_user(self, username):
        return await self.bot.db.fetch("SELECT * FROM users WHERE username = $1", username)

    async def get_user_by_id(self, user_id):
        return await self.bot.db.fetch("SELECT * FROM users WHERE user_id = $1", user_id)

    async def add_user(self, username=None, pray_count=0, user_id=None, xp=0, level=0):
        await self.bot.db.execute("""INSERT INTO users (username, pray_count, user_id, current_xp, level) \
         VALUES ($1, $2, $3, $4, $5)""", username, pray_count, user_id, xp, level)

    async def add_pray(self, username, user_id=None):
        await self.bot.db.execute("""INSERT INTO pray_logs (username, timestamp, user_id) VALUES ($1, $2, $3)""", username,
                                  datetime.datetime.utcnow(), user_id)

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
            """SELECT * FROM pray_logs WHERE timestamp > DATE_TRUNC('week', NOW())""")

    async def get_last_pray_user(self, user):
        return await self.bot.db.fetch(
            """SELECT * FROM pray_logs WHERE username = $1 ORDER BY timestamp DESC LIMIT 1""",
            user)

    async def update_user_id(self, user_id, username):
        await self.bot.db.execute("""UPDATE users SET user_id = $1 WHERE username = $2""", user_id, username)

    async def set_user_xp(self, user, xp):
        if isinstance(user, int):  # check if user is id
            await self.bot.db.execute("""UPDATE users SET current_xp = $1 WHERE user_id = $2""", xp, user)
            return

        await self.bot.db.execute("""UPDATE users SET current_xp = $1 WHERE username = $2""", xp, user)

    async def set_user_level(self, user, lvl):
        if isinstance(user, int):  # check if user is id
            await self.bot.db.execute("""UPDATE users SET level = $1 WHERE user_id = $2""", lvl, user)
            return

        await self.bot.db.execute("""UPDATE users SET level = $1 WHERE username = $2""", lvl, user)

    async def get_level_leaderboard(self):
        return await self.bot.db.fetch("""SELECT * FROM users ORDER BY level DESC""")


def setup(bot):
    bot.add_cog(Database(bot))

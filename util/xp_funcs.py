import math


class Util():

    def __init__(self, bot):
        self.bot = bot
        self.XP_MULTI = 5

    def check_level_up(self, user_xp, level):
        required_xp = 5000 + math.pow(level * self.XP_MULTI, 2)

        if user_xp >= required_xp:
            return True

        return False

    async def distribute_rewards(self, user, user_lvl):
        louis_dm = await self.bot.fetch_user(289411794672418819)
        if isinstance(user, int):
            await louis_dm.send(f"`owogive <@{user}> {user_lvl * 25000}`")
            await louis_dm.send(f"{user} levelled up to level {user_lvl}")
            return

        await louis_dm.send(f"`owogive {user} {user_lvl * 25000}`")
        await louis_dm.send(f"{user} levelled up to level {user_lvl}")
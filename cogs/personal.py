from discord.ext import commands
import math


class Personal(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile", aliases=["p"])
    async def profile(self, ctx):

        user = await self.bot.hdb.get_user([ctx.author.id, ctx.author.name])
        user_lvl = user[0]["level"]
        user_xp = user[0]["current_xp"]
        required_xp = 5000 + math.pow(user_lvl * self.bot.util.XP_MULTI, 2)
        progress = ("■" * ((user_xp / required_xp) * 10)).rjust(10, "□")
        await ctx.channel.send(f"level: {user_lvl} progress: [{user_xp}/{required_xp}] {progress}")


def setup(bot):
    bot.add_cog(Personal(bot))
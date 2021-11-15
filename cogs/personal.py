from discord.ext import commands
import math
import discord


class Personal(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile", aliases=["p"])
    async def profile(self, ctx):

        user = await self.bot.hdb.get_user(ctx.author.name)
        user_lvl = user[0]["level"]
        user_xp = user[0]["current_xp"]
        required_xp = 5000 + math.pow(user_lvl * self.bot.util.XP_MULTI, 2)
        progress = ("■" * int((user_xp / required_xp) * 10)).ljust(10, "□")

        embed = discord.Embed()
        embed.set_author(name=f"**{ctx.author.name}'s profile**", icon_url=str(ctx.author.avatar_url))
        embed.add_field(name="Level", value=user_lvl)
        embed.add_field(name="Experience", value=f"[{user_xp}/{required_xp}]\n{progress}")

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Personal(bot))
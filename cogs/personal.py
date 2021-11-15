from discord.ext import commands
import math
import discord


class Personal(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile", aliases=["p", "pp"])
    async def profile(self, ctx):

        # what the fuck is this
        progress_bar_full_1 = "<a:Bar1Full:909895429540421672>"
        progress_bar_full_2 = "<a:Bar2Full:909895429322313850>"
        progress_bar_empty_1 = "<:Bar1Empty:909897948698128395>"
        progress_bar_empty_2 = "<:Bar2Empty:909895429217460265>"
        progress_bar_empty_3 = "<:Bar3Empty:909895429540429844> "

        user = await self.bot.hdb.get_user(ctx.author.name)
        user_lvl = user[0]["level"]
        user_xp = user[0]["current_xp"]
        required_xp = int(5000 + math.pow(user_lvl * self.bot.util.XP_MULTI, 2))
        progress = (progress_bar_full_2 * int((user_xp / required_xp) * 10)).ljust(8, progress_bar_empty_2)

        if progress_bar_full_2 in progress:
            progress = progress_bar_full_1 + progress

        else:
            progress = progress_bar_empty_1 + progress + progress_bar_empty_3

        if progress == progress_bar_empty_2 * 8:

            progress += progress_bar_full_2

        embed = discord.Embed(color=discord.Color.orange())
        embed.set_author(name=f"{ctx.author.name}'s profile", icon_url=str(ctx.author.avatar_url))
        embed.set_thumbnail(url=str(ctx.author.avatar_url))
        embed.add_field(name="Level", value="`" + str(user_lvl) + "`")
        embed.add_field(name="Experience", value=f"`[{user_xp}/{required_xp}]`\n{progress}")

        await ctx.channel.send(embed=embed)
        await ctx.channel.send(progress_bar_full_1 + ' ' + progress_bar_full_2 + ' ' + progress_bar_empty_1 + ' ' + progress_bar_empty_2 + ' ' + progress_bar_empty_3)


def setup(bot):
    bot.add_cog(Personal(bot))
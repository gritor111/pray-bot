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

        user = await self.bot.hdb.get_user(ctx.author.id)
        user_lvl = user["level"]
        user_xp = user["current_xp"]
        required_xp = int(5000 + math.pow(user_lvl * self.bot.util.XP_MULTI, 2))

        progress = ("■" * int((user_xp / required_xp) * 10)).ljust(10, "□")

        #  i made this logic at like 1am dont judge me

        if "■" in progress:
            progress = list(progress)
            progress[0] = progress_bar_full_1
            progress = ''.join(progress)

        else:
            progress = list(progress)
            progress[0] = progress_bar_empty_1  # replace first char
            progress = ''.join(progress)

        progress = list(progress)
        progress[-1] = progress_bar_empty_3  # replace last char
        progress = ''.join(progress)

        progress = progress.replace("■", progress_bar_full_2)
        progress = progress.replace("□", progress_bar_empty_2)

        embed = discord.Embed(color=discord.Color.orange())
        embed.set_author(name=f"{ctx.author.name}'s profile", icon_url=str(ctx.author.avatar_url))
        embed.set_thumbnail(url=str(ctx.author.avatar_url))
        embed.add_field(name="Level", value="`" + str(user_lvl) + "`", inline=False)
        embed.add_field(name="Experience", value=f"`{user_xp}/{required_xp}`\n{progress}", inline=False)

        await ctx.channel.send(embed=embed)

    # @commands.command(name="claim")
    # async def claim(self, ctx):
    #     unclaimed_prays = self.bot.hdb.get_unclaimed_prays(ctx.author.id)

def setup(bot):
    bot.add_cog(Personal(bot))
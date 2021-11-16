from discord.ext import commands
import discord


class HelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):

        ctx = self.get_destination()
        embed = discord.Embed(color=discord.Color.teal())
        embed.set_author(name="Bot Help", icon_url=str(ctx.author.avatar_url))

        for cog in mapping:
            embed.add_field(name=cog.name, value=' '.join(['`' + command.name + '`' for command in cog.get_commands()]),
                            inline=False)

        await self.send(embed=embed)

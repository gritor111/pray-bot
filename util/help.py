from discord.ext import commands
import discord


class HelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        print(mapping)
        embed = discord.Embed(color=discord.Color.teal())
        embed.set_author(name="Bot Help", icon_url=str(self.context.author.avatar_url))

        for cog in mapping:
            embed.add_field(name=cog.qualified_name, value=' '.join(['`' + command.name + '`' for command in cog.get_commands()]),
                            inline=False)

        await self.send(embed=embed)

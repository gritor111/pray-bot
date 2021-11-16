from discord.ext import commands
import discord


class HelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):

        embed = discord.Embed(color=discord.Color.teal())
        embed.set_author(name="Bot Help", icon_url=str(self.context.author.avatar_url))

        for cog in mapping:
            if cog and mapping[cog] and cog.qualified_name != "Owner":
                embed.add_field(name=cog.qualified_name,
                                value=' '.join(['`' + command.name + '`' for command in mapping[cog]]),
                                inline=False)

        await self.context.channel.send(embed=embed)

    async def send_group_help(self, group):

        embed = discord.Embed(color=discord.Color.teal())
        embed.set_author(name=f"{group.name} Help", icon_url=str(self.context.author.avatar_url))

        embed.add_field(name=f"{group.name} commands",
                        value=' '.join(['`' + command.name + '`' for command in group.commands]))

        await self.context.channel.send(embed=embed)




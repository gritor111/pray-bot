from discord.ext import commands
import discord


class HelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):

        ctx = self.context
        embed = discord.Embed(color=discord.Color.teal())
        embed.set_author(name="Bot Help", icon_url=str(self.context.author.avatar_url))

        for cog in mapping:
            if cog and mapping[cog] and cog.qualified_name != "Owner":
                embed.add_field(name=cog.qualified_name,
                                value=' '.join(['`' + command.name + '`' for command in mapping[cog]]),
                                inline=False)

        await ctx.channel.send(embed=embed)

    async def send_group_help(self, group):

        ctx = self.context
        embed = discord.Embed(color=discord.Color.teal())
        embed.set_author(name=f"{group.name.capitalize()} Help", icon_url=str(self.context.author.avatar_url))

        embed.add_field(name=f"{group.name.capitalize()} commands",
                        value=' '.join(['`' + command.name + '`' for command in group.commands]))

        await ctx.channel.send(embed=embed)

    async def send_command_help(self, command):

        ctx = self.context
        print(ctx.bot.user)
        # embed = discord.Embed(color=discord.Color.teal())
        # embed.set_author(name=f"{command.name.capitalize()} Usage",
        #                  icon_url=str(self.context.author.avatar_url),
        #                  description=f"{self.bot.}")






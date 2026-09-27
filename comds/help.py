import discord
from discord.ext import commands
from discord import app_commands


class CustomHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__(verify_checks=False)

    def get_command_signature(self, command: commands.Command) -> str:
        base = f"{self.context.prefix}{command.qualified_name}"
        if command.signature:
            return f"{base} {command.signature}"
        return base

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", description="List of commands:", color=discord.Color.blue())
        for cog, commands_list in mapping.items():
            name = "General" if cog is None else getattr(cog, "qualified_name", cog.__class__.__name__)
            lines = []
            for command in commands_list:
                if command.hidden:
                    continue
                desc = command.help or command.short_doc or "No description."
                lines.append(f"`{self.get_command_signature(command)}` — {desc}")
            if lines:
                embed.add_field(name=name, value="\n".join(lines), inline=False)
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f"{cog.qualified_name} Commands", color=discord.Color.blue())
        lines = []
        for command in cog.get_commands():
            if command.hidden:
                continue
            desc = command.help or command.short_doc or "No description."
            lines.append(f"`{self.get_command_signature(command)}` — {desc}")
        if lines:
            embed.add_field(name=cog.qualified_name, value="\n".join(lines), inline=False)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Help — {command.qualified_name}", color=discord.Color.blue())
        embed.add_field(name="Usage", value=f"`{self.get_command_signature(command)}`", inline=False)
        embed.add_field(name="Description", value=command.help or "No description.", inline=False)
        await self.get_destination().send(embed=embed)


class HelpCog(commands.Cog):
    """Provides a slash `/help` that shows the same information as the prefix help."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="List all commands and their descriptions")
    async def slash_help(self, interaction: discord.Interaction):
        mapping = {}
        # collect commands from cogs
        for cog in self.bot.cogs.values():
            mapping[cog] = [c for c in cog.get_commands() if not c.hidden]
        # uncategorized commands
        uncategorized = [c for c in self.bot.commands if c.cog is None and not c.hidden]
        if uncategorized:
            mapping[None] = uncategorized

        embed = discord.Embed(title=f"{getattr(self.bot.user, 'name', 'Bot')} — Help", description="List of commands:", color=discord.Color.blue())
        for cog, commands_list in mapping.items():
            name = "General" if cog is None else getattr(cog, "qualified_name", cog.__class__.__name__)
            lines = []
            for command in commands_list:
                # show prefix-style signature; slash command signature is out of scope here
                prefix = self.bot.command_prefix if isinstance(self.bot.command_prefix, str) else ""
                sig = f"{prefix}{command.qualified_name} {command.signature}".strip()
                desc = command.help or command.short_doc or "No description."
                lines.append(f"`{sig}` — {desc}")
            if lines:
                embed.add_field(name=name, value="\n".join(lines), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    bot.help_command = CustomHelp()
    await bot.add_cog(HelpCog(bot))

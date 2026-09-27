import discord 
from discord.ext import commands
import os
import dotenv 
from dotenv import load_dotenv
from typing import Optional
from comds.help import CustomHelp
import config


load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.prefix, intents=intents, help_command=CustomHelp())   


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')
    await bot.tree.sync()

@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")



bot.run(config.token)
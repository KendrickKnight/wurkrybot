import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from time import sleep
import json
import sys
import subprocess

import util

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf8', mode='w')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)



bot.run(token, log_handler=handler, log_level=logging.DEBUG)
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

# bot = commands.Bot(command_prefix='!', intents=intents)


# def load_data


class MyBot(commands.bot):

    def __init__(self,**kwargs):
        super().__init__(self,**kwargs)



    async def setup_hook(self):
        # self.bot.create_task(load_data())
        await self.load_extension("cogs.c_util")

    


bot = MyBot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"{bot.user.name}, ready to rumble >:D")


@bot.on_guild_join()





def main():

    bot.run(token, log_handler=handler, log_level=logging.DEBUG)
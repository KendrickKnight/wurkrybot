import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

import util

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf8', mode='w')


class MyBot(commands.Bot):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.data_lobbbies = {}
        self.data_settings = {}

    async def setup_hook(self):
        # Server settings
        self.data_settings = util.syncData("settings")
        
        # Lobby update loop
        self.loop.create_task(self.update_lobbies())
              
        # self.bot.create_task(load_data())
        await self.load_extension("cogs.c_util")
        await self.load_extension("cogs.c_test")
        await self.load_extension("cogs.c_dev")
        await self.load_extension("cogs.c_lobby")
        await self.load_extension("cogs.c_map_filter")



    async def update_lobbies(self):
        while True:
            try:
                self.data_lobbies = util.syncData("lobbies")
            except Exception as e:
                print(e)
            await asyncio.sleep(5)


intents = discord.Intents.default()
intents.message_content = True


bot = MyBot(command_prefix="!",intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name}, ready to rumble >:D")


# @bot.on_guild_join()





bot.run(token, log_handler=handler, log_level=logging.DEBUG)

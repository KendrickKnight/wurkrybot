import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import challonge

import util

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf8', mode='w')


class MyBot(commands.Bot):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        # Data
        self.data_lobbbies = {}
        self.data_settings = {}
        self.data_notifs = {}
        self.data_tournaments = {"pending": {}, "in_progress": {}, "ended": {}}

        # Challonge
        self.challonge_api = "https://api.challonge.com/v1/"
        self.challonge_token = os.getenv('CHALLONGE_TOKEN')
        self.challonge_name = "Kendrickknight"
    
    async def setup_hook(self):
        # Server settings
        self.data_settings = util.syncData("settings")
        
        # Update loops
        self.loop.create_task(self.update_lobbies())
        self.loop.create_task(self.update_tournaments())

        # Challonge API Credentials
        challonge.set_credentials(self.challonge_name,self.challonge_token)
              
        # Load Cogs
        await self.load_extension("cogs.c_util")
        await self.load_extension("cogs.c_test")
        await self.load_extension("cogs.c_dev")
        await self.load_extension("cogs.c_lobby")
        await self.load_extension("cogs.c_events")
        await self.load_extension("cogs.c_challonge")
        await self.load_extension("cogs.c_map_filter")



    async def update_lobbies(self):
        while True:
            try:
                self.data_lobbies = util.syncData("lobbies")
            except Exception as e:
                print(e)
            await asyncio.sleep(5)

    async def update_tournaments(self):

        # TODO:
            # [ ] Sort each tournament based on time
            # [ ] If teams == True, add teams to the tournament data
        
        while True:
            try:

                
                if challonge.tournaments.index() == []:
                    continue
                
                for tournament in challonge.tournaments.index():

                    for key in self.data_tournaments:
                        if tournament["id"] in self.data_tournaments[key]:
                            continue

                    
                    # I dont want every single piece of data, so I will only take what I need
                    data_desired = ["id","name","game_name",
                                    "url","description","tournament_type",
                                    "state","participants_count","teams",
                                    "team_size_range","start_at","registration_type",
                                    "full_challonge_url","live_image_url","sign_up_url"]
                    data_tournament = {}

                    for key in data_desired:
                        data_tournament[key] = tournament[key]
                        
                    
                    self.data_tournaments[tournament["id"]] = data_tournament

                
            except Exception as e:
                print(e)
            await asyncio.sleep(5)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = MyBot(command_prefix="!",intents=intents)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

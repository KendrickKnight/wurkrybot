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
        self.data_lobbbies = {}
        self.data_settings = {}
        self.data_notifs = {}

        self.data_tournaments = {}
        self.challonge_api = "https://api.challonge.com/v1/"
        self.challonge_token = os.getenv('CHALLONGE_TOKEN')
        self.challonge_name = "Kendrickknight"


    
    async def setup_hook(self):
        # Server settings
        self.data_settings = util.syncData("settings")
        
        # Lobby & Tournament update loop
        self.loop.create_task(self.update_lobbies())
        self.loop.create_task(self.update_tournaments())

        # Tournament update loop
        challonge.set_credentials(self.challonge_name,self.challonge_token)
              
        # self.bot.create_task(load_data())
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

        # Data_Tournament:
        #     ID 
        #     Name 
        #     Game_name
        #     URL
        #     Description
        #     Tournament_type
        #     State (pending/canceled/started/finished… whatever is possible)
        #     Participants_count
        #     Teams (True/False)
        #     Team_size_range
        #     Start_at 
        #     Registration_type
        #     Full_challonge_url
        #     Libe_image_url
        #     Sign_up_url

        
        while True:
            try:
                # self.data_tournaments = challonge.tournaments.index()

                for tournament in challonge.tournaments.index():
                    if tournament["id"] in self.data_tournaments:
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

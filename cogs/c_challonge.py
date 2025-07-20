import discord
from discord.ext import commands
import asyncio 
from dotenv import load_dotenv
import os

load_dotenv()

# TODO: 
    # [ ] Message function, that creates tournament embeds
    # [ ] Sorting function to sort and find closest tournament time wise

class Tournament(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    def msg_embed_tournament(self,ctx,tournament):
        pass

    def sort_tournaments(self,ctx):
        pass

    @commands.command(brief="[M] Shows all tournaments.")
    async def tourn_display(self,ctx):
        print(self.bot.data_tournaments)
        pass
        
        

async def setup(bot):
    await bot.add_cog(Tournament(bot))
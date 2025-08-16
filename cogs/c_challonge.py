import discord
from discord.ext import commands
import asyncio 
from dotenv import load_dotenv
import os

load_dotenv()

# TODO: 
    # msg_embed_tournament()
        # Tournament Name [Tournament Type]
        # *Tournament ID*
        # Tournament Description
        # Participents [Participents Count]
            # Participents list

    # report_tournament(id)
        # IF id is in argument, report only that tournament
        # ELSE report all tournaments

        # Embed message for each tournament
        # Get the message in need of edit
        # Edit the message

class Tournament(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    
        
        

async def setup(bot):
    await bot.add_cog(Tournament(bot))
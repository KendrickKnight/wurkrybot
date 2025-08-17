from challonge import participants
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

    def msg_embed_tournament(self,ctx,tournament):
        # Participants list in text format
        participants = "\n".join([f"{participant['name']}" for participant in tournament["participants"]])
        
        embed = discord.Embed(
            title=f"{tournament['name']} [{tournament['tournament_type']}]",
            description=f"ID: {tournament['id']} \n{tournament['description']}",
            colour=discord.Colour.blue()
        )
        embed.add_field(name=f"Participents [{tournament['participants'].count()}]", value=f"{participants}", inline=True)

        return embed
        
        

async def setup(bot):
    await bot.add_cog(Tournament(bot))
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


    def msg_embed_tournament_single(self,ctx,tournament):
        name = tournament["name"]
        description = tournament["description"]

        embed = discord.Embed(
            title=f"{name}",
            description=f"{description}",
            colour=discord.Colour.blue()
        )

        # Text for listing participants
        participants = ""
        participants_count = 1
        for participant in tournament["participants"]:
            participants += f"{participants_count}. {participant['name']}\n"
            participants_count += 1
        
        embed.add_field(name="Participants", value=participants, inline=True)
        embed.set_thumbnail(url="https://placehold.co/300/2F3136/2F3136")

        return embed


    # TODO: 
        # Store Teams in a list somewhere 
        # Display teams in embed instead of participants
            # Display team members in () after team name. like: KnightSiders (K-el, ledarsi, ConscouslyEating)
    def msg_embed_tournament_team(self,ctx,tournament):
        name = tournament["name"]
        description = tournament["description"]

        embed = discord.Embed(
            title=f"{name}",
            description=f"{description}",
            colour=discord.Colour.blue()
        )
        embed.add_field(name="Teams", value="", inline=True)
        embed.set_thumbnail(url="https://placehold.co/300/2F3136/2F3136")

        return embed
    
    def sort_tournaments(self,ctx):
        pass

    @commands.command(brief="[M] Shows all tournaments.")
    async def trn_display(self,ctx):
        print(self.bot.data_tournaments)
        pass
        
        

async def setup(bot):
    await bot.add_cog(Tournament(bot))
from discord.ext import commands

class UtilCog(commands.cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def hi(self,ctx):
        await ctx.send(f"hello {ctx.author.mention}")
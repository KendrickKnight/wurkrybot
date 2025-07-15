from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def hi(self,ctx):
        await ctx.send(f"hello {ctx.author.mention}")



async def setup(bot):
    await bot.add_cog(Utility(bot))
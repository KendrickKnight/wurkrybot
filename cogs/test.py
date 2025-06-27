from discord.ext import commands

class Test(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hit(self, ctx):
        await ctx.send(f"IM HIT! the cog also works btw.")
    

async def setup(bot):
    await bot.add_cog(Test(bot))
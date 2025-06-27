from discord.ext import commands

class Test(commands.cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hit(self, ctx):
        await ctx.send(f"IM HIT! the cog also works btw.")
    

def setup(bot):
    bot.add_cog(Test(bot))
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test_settings(self,ctx):
        await ctx.send(self.bot.data_settings)

async def setup(bot):
    await bot.add_cog(Test(bot))
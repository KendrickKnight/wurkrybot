from discord.ext import commands

class Bot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def wurk_add_settings(self,ctx):
        guild = ctx.guild.id
        self.bot.data_settings[guild] = {"roles":{}}
        await ctx.send("Settings added")
        

async def setup(bot):
    await bot.add_cog(Bot(bot))
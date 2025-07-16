from discord.ext import commands
import util

class Bot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def wurk_add_settings(self,ctx):
        guild = str(ctx.guild.id)
        if guild in self.bot.data_settings:
            await ctx.send("Settings already exist")
        else:
            self.bot.data_settings[guild] = {
                "notify":True,
                "roles":{}
            }
            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)
            await ctx.send("Settings added")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def wurk_show_settings(self,ctx):
        guild = str(ctx.guild.id)
        try:
            await ctx.send(self.bot.data_settings[guild])
            await ctx.send(len(self.bot.data_settings[guild]["roles"]))
        except Exception as e:
            await ctx.send(f"error: \n{e}")

async def setup(bot):
    await bot.add_cog(Bot(bot))




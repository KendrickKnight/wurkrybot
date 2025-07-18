from discord.ext import commands
import asyncio
import util

class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def hi(self,ctx):
        await ctx.send(f"> hello {ctx.author.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self,ctx):
        await ctx.channel.purge()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def notifToggle(self,ctx):
        guild_id = str(ctx.guild.id)
        if guild_id in self.bot.data_settings:
            
            notif_state = self.bot.data_settings[guild_id]["notify"] 
            notif_state = notif_state
            
            self.bot.data_settings[guild_id]["notify"] = notif_state
            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)
            
            if notif_state:
                msg_notif_state = await ctx.send("> Notifications enabled")
                await asyncio.sleep(5)
                await msg_notif_state.delete()
            else:
                msg_notif_state = await ctx.send("> Notifications disabled")
                await asyncio.sleep(5)
                await msg_notif_state.delete()
            
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def roles(self,ctx):
        guild_id = str(ctx.guild.id)
        if guild_id in self.bot.data_settings:
            await ctx.send(self.bot.data_settings[guild_id]["roles"])
        else:
            await ctx.send("> No roles found")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self,ctx):
        guild_id = str(ctx.guild.id)
        if guild_id in self.bot.data_settings:
            self.bot.data_settings[guild_id] = {
                "notify":True,
                "roles":{
                    "ranked" : {"map": None,
                                "color": "d62411",
                                "img": "https://placehold.co/300/2F3136/2F3136",
                                "emoji": "🏆"}
                }
            }
            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)
            msg_reset = await ctx.send("> Settings reset")
            await asyncio.sleep(5)
            await msg_reset.delete()

async def setup(bot):
    await bot.add_cog(Utility(bot))
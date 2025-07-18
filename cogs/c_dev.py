from discord.ext import commands
import asyncio
import util
import os
import sys

class Dev(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(brief="[D] Shuts down the bot (owner only).",hidden=True)
    @commands.is_owner()
    async def dev_shutdown_bot(self, ctx: commands.Context):
        """Shuts down the bot (owner only)."""
        await ctx.send("> Shutting down...")
        await self.bot.close()  # cleanly close the bot

    @commands.command(brief="[D] Restarts the bot (owner only).",hidden=True)
    @commands.is_owner()
    async def dev_restart_bot(self, ctx: commands.Context):
        """Restarts the bot (owner only)."""
        await ctx.send("> Restarting bot...")

        # close bot
        await self.bot.close()

        # schedule the restart after closing
        python = sys.executable
        os.execl(python, python, *sys.argv)

    
    @commands.command(brief="[D] Reloads all cogs (owner only).",hidden=True)
    @commands.is_owner()
    async def dev_reload(self,ctx):
        await self.bot.reload_extension("cogs.c_util")
        await self.bot.reload_extension("cogs.c_test")
        await self.bot.reload_extension("cogs.c_lobby")
        await self.bot.reload_extension("cogs.c_map_filter")

        msg_reload = await ctx.send("> Reloaded all cogs")
        await asyncio.sleep(5)
        await msg_reload.delete()
        
    @commands.command(brief="[D] Adds settings for the server (owner only).",hidden=True)
    @commands.is_owner()
    async def dev_add_settings(self,ctx):
        guild = str(ctx.guild.id)
        if guild in self.bot.data_settings:
            await ctx.send("> Settings already exist")
        else:
            self.bot.data_settings[guild] = {
                "notify":True,
                "roles":{
                    "ranked" : {"map": None,
                                "color": "d62411",
                                "img": "https://placehold.co/300/2F3136/2F3136",
                                "emoji": "🏆"}
                }
            }
            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)
            await ctx.send("> Settings added")

    @commands.command(brief="[D] shows this server's json settings (owner only).",hidden=True)
    @commands.is_owner()
    async def dev_show_settings(self,ctx):
        guild = str(ctx.guild.id)
        try:
            await ctx.send(">>> "+ self.bot.data_settings[guild])
            await ctx.send("> "+ str(len(self.bot.data_settings[guild]["roles"])))
        except Exception as e:
            await ctx.send(f">>> error: \n{e}")



async def setup(bot):
    await bot.add_cog(Dev(bot))
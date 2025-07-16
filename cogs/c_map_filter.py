import discord
from discord.ext import commands
import random
import util
import asyncio

class MapFilter(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.default_img = "https://placehold.co/300/2F3136/2F3136"
        self.colors = {
            1 : "16171a",
            2 : "7f0622",
            3 : "d62411",
            4 : "ff8426",
            5 : "ffd100",
            6 : "fafdff",
            7 : "ff80a4",
            8 : "ff2674",
            9 : "94216a",
            10: "430067",
            11: "234975",
            12: "68aed4",
            13: "bfff3c",
            14: "10d275",
            15: "007899",
            16: "002859"
        }
    
    @commands.command()
    async def mapf_view(self,ctx):
            
        guild_id = str(ctx.guild.id)
        message = "## Map Filters \n"
        
        try:
            if len(self.bot.data_settings[guild_id]["roles"]) == 0:
                message += "No map filters set"
            else:
                for role in self.bot.data_settings[guild_id]["roles"]:
                    message += f"**{role}** : {self.bot.data_settings[guild_id]['roles'][role]['map']} \n"
    
            await ctx.send(message)
        except Exception as e:
            await ctx.send(f"your server is not setup yet. use wurk_add_settings to add your server. \n{e}")
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mapf_add(self,ctx,role_name,map_name = None,color = None,img = None):
        guild_id = str(ctx.guild.id)

        if map_name is None:
            map_name = role_name
        if color is None:
            color = self.colors[random.randint(1,16)]
        if img is None:
            img = self.default_img
            
        try:
            self.bot.data_settings[guild_id]["roles"][role_name] = {"map":map_name,"color":color,"img":img}
            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)

            await ctx.guild.create_role(name=role_name)
            
            msg_filter_add = await ctx.send(f"Map filter added for {role_name} with map {map_name}")
            await asyncio.sleep(5)
            await msg_filter_add.delete()
        
        except Exception as e:
            await ctx.send(f"error: \n{e}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mapf_remove(self,ctx,role_name):
        guild_id = str(ctx.guild.id)

        if role_name in self.bot.data_settings[guild_id]["roles"]:
            del self.bot.data_settings[guild_id]["roles"][role_name]
            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)

            guild_role = discord.utils.get(ctx.guild.roles, name=role_name)
            if guild_role:
                await guild_role.delete()
                msg_filter_remove = await ctx.send(f"Map filter removed for {role_name}")
                await asyncio.sleep(5)
                await msg_filter_remove.delete()
            else:
                await ctx.send(f"filter {role_name} but the role does not exist")
            
        else:
            await ctx.send(f"Map filter for {role_name} does not exist")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mapf_att(self,ctx,role_name,color,img):
        guild_id = str(ctx.guild.id)
        if role_name in self.bot.data_settings[guild_id]["roles"]:
            self.bot.data_settings[guild_id]["roles"][role_name]["color"] = color
            self.bot.data_settings[guild_id]["roles"][role_name]["img"] = img
            
            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)
            
            await ctx.send(f"Map filter attributes updated for {role_name}")
        else:
            await ctx.send(f"The filter{role_name} doesnt exist")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mapf_color(self,ctx,role_name,color):
        guild_id = str(ctx.guild.id)
        if role_name in self.bot.data_settings[guild_id]["roles"]:
            self.bot.data_settings[guild_id]["roles"][role_name]["color"] = color

            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)

            await ctx.send(f"Map filter attributes updated for {role_name}")
        else:
            await ctx.send(f"The filter{role_name} doesnt exist")






    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mapf_img(self,ctx,role_name,img):
        guild_id = str(ctx.guild.id)
        if role_name in self.bot.data_settings[guild_id]["roles"]:
            self.bot.data_settings[guild_id]["roles"][role_name]["img"] = img

            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)

            await ctx.send(f"Map filter attributes updated for {role_name}")
        else:
            await ctx.send(f"The filter{role_name} doesnt exist")




async def setup(bot):
    await bot.add_cog(MapFilter(bot))




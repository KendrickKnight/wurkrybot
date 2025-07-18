import discord
from discord.ext import commands
import random
import util
import asyncio

class MapFilter(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.default_img = "https://dummyimage.com/300x300/131416/131416.png"
        self.colors = {
            1 : "16171a",
            2 : "7f0622",
            3 : "002859",
            4 : "ff8426",
            5 : "ffd100",
            6 : "007899",
            7 : "ff80a4",
            8 : "ff2674",
            9 : "94216a",
            10: "430067",
            11: "234975",
            12: "68aed4",
            13: "bfff3c",
            14: "10d275",
        }
        self.emojis ={
            "🤠" : False,
            "😎" : False,
            "👾" : False,
            "🎱" : False,
            "🍥" : False,
            "⚓" : False,
            "🛡️" : False,
            "🧭" : False,
            "♦️" : False,
            "🔥" : False,
            "🎩" : False,

        }
    
    @commands.command(brief="[A] Shows all map filters.")
    @commands.has_permissions(administrator=True)
    async def mapf_view(self,ctx):
            
        guild_id = str(ctx.guild.id)
        message = "## Map Filters \n"
        
        try:
            if len(self.bot.data_settings[guild_id]["roles"]) == 0:
                message += ">>> No map filters set"
            else:
                for role in self.bot.data_settings[guild_id]["roles"]:
                    message += f"**{role}** : {self.bot.data_settings[guild_id]['roles'][role]['map']} \n"
    
            await ctx.send(message)
        except Exception as e:
            await ctx.send(f"> your server is not setup yet. use wurk_add_settings to add your server. \n{e}")

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def mapf_ranked(self,ctx):
    #     guild_id = str(ctx.guild.id)
    #     guild_roles = [role.name.lower() for role in ctx.guild.roles]
    #     role_name = "ranked"
    #     roles = [role.lower() for role in self.bot.data_settings[guild_id]["roles"]]
        
    #     if role_name in roles:
    #         ranked_state = self.bot.data_settings[guild_id]["roles"][role_name]
    #         ranked_state = not ranked_state
    #         util.syncData("settings",cmd=False,inputData=self.bot.data_settings)
            
    #         if ranked_state:
    #             if role_name not in guild_roles:
    #                 await ctx.guild.create_role(name=role_name)
    
    #             msg_ranked_state = await ctx.send("Ranked filter enabled")
    #             await asyncio.sleep(5)
    #             await msg_ranked_state.delete()
                
    #         else:
    #             if role_name in guild_roles:
    #                 guild_role = discord.utils.get(ctx.guild.roles, name="Ranked")
    #                 await guild_role.delete()
                    
    #             msg_ranked_state = await ctx.send("Ranked filter disabled")
    #             await asyncio.sleep(5)
    #             await msg_ranked_state.delete()
            

    
    @commands.command(brief="[A] Adds a map filter.",help="!mapf_add <role_name> <map_name> <color> <img> <emoji>")
    @commands.has_permissions(administrator=True)
    async def mapf_add(self,ctx,role_name,map_name = None,color = None,img = None,emoji=None):
        guild_id = str(ctx.guild.id)
        await ctx.message.delete()
        
        if map_name is None:
            map_name = role_name.lower()
        if color is None:
            color = self.colors[random.randint(1,14)]
        if img is None:
            img = self.default_img
        if emoji is None:
            emoji = random.choice(list(self.emojis.keys()))
            while self.emojis[emoji]: # this is to make sure that the emoji is not already in use
                emoji = random.choice(list(self.emojis.keys())) 
            self.emojis[emoji] = True
            
        try:
            self.bot.data_settings[guild_id]["roles"][role_name] = {"map":map_name.lower(),"color":color,"img":img,"emoji":emoji}
            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)

            if role_name not in self.bot.data_notifs[guild_id]:
                self.bot.data_notifs[guild_id][role_name] = False

            await ctx.guild.create_role(name=role_name)
            
            msg_filter_add = await ctx.send(f"> Map filter added for {role_name} with map {map_name}")
            await asyncio.sleep(5)
            await msg_filter_add.delete()
        
        except Exception as e:
            await ctx.send(f"error: \n{e}")

    @commands.command(brief="[A] Removes a map filter.",help="!mapf_remove <role_name>")
    @commands.has_permissions(administrator=True)
    async def mapf_remove(self,ctx,role_name):
        guild_id = str(ctx.guild.id)
        await ctx.message.delete()
        
        if role_name in self.bot.data_settings[guild_id]["roles"]:
            guild_role = discord.utils.get(ctx.guild.roles, name=role_name)
            
            self.emojis[self.bot.data_settings[guild_id]["roles"][role_name]["emoji"]] = False
            
            del self.bot.data_settings[guild_id]["roles"][role_name]
            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)

            if role_name in self.bot.data_notifs[guild_id]:
                del self.bot.data_notifs[guild_id][role_name]
            
            if guild_role:
                
                await guild_role.delete()
                
                msg_filter_remove = await ctx.send(f"> Map filter removed for {role_name}")
                await asyncio.sleep(5)
                await msg_filter_remove.delete()
            else:
                await ctx.send(f"> filter {role_name} but the role does not exist")
            
        else:
            await ctx.send(f"> Map filter for {role_name} does not exist. \nthis command is case sensitive. make sure you are using the correct case.")


    @commands.command(brief="[A] Changes the attributes of a map filter. Use if you want to change every attribute!",help="!mapf_att <role_name> <color> <img> <emoji>. ")
    @commands.has_permissions(administrator=True)
    async def mapf_att(self,ctx,role_name,color,img,emoji):
        guild_id = str(ctx.guild.id)
        if role_name in self.bot.data_settings[guild_id]["roles"]:
            self.bot.data_settings[guild_id]["roles"][role_name]["color"] = color
            self.bot.data_settings[guild_id]["roles"][role_name]["img"] = img
            self.bot.data_settings[guild_id]["roles"][role_name]["emoji"] = emoji

            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)
            
            await ctx.send(f"> Map filter attributes updated for {role_name}")
        else:
            await ctx.send(f"> The filter{role_name} doesnt exist")


    @commands.command(brief="[A] Changes the color of a map filter.",help="!mapf_color <role_name> <color>")
    @commands.has_permissions(administrator=True)
    async def mapf_color(self,ctx,role_name,color):
        guild_id = str(ctx.guild.id)
        if role_name in self.bot.data_settings[guild_id]["roles"]:
            self.bot.data_settings[guild_id]["roles"][role_name]["color"] = color

            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)

            await ctx.send(f"> Map filter stripe color updated for {role_name}")
        else:
            await ctx.send(f"> The filter{role_name} doesnt exist")






    @commands.command(brief="[A] Changes the img of a map filter.",help="!mapf_color <role_name> <img>")
    @commands.has_permissions(administrator=True)
    async def mapf_img(self,ctx,role_name,img):
        guild_id = str(ctx.guild.id)
        if role_name in self.bot.data_settings[guild_id]["roles"]:
            self.bot.data_settings[guild_id]["roles"][role_name]["img"] = img

            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)

            await ctx.send(f"> Map filter image updated for {role_name}")
        else:
            await ctx.send(f"> The filter{role_name} doesnt exist")


    @commands.command(brief="[A] Changes the emoji of a map filter.",help="!mapf_color <role_name> <emoji>")
    @commands.has_permissions(administrator=True)
    async def mapf_emoji(self,ctx,role_name,emoji):
        guild_id = str(ctx.guild.id)
        if role_name in self.bot.data_settings[guild_id]["roles"]:
            self.bot.data_settings[guild_id]["roles"][role_name]["emoji"] = emoji

            util.syncData("settings",cmd=False,inputData=self.bot.data_settings)

            await ctx.send(f"> Map filter emoji updated for {role_name}")
        else:
            await ctx.send(f"> The filter{role_name} doesnt exist")



async def setup(bot):
    await bot.add_cog(MapFilter(bot))




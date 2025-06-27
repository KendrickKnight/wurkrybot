import discord
from discord.ext import commands
from time import sleep
import json
import msg_funcs as msf

class Lobby(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help = "[Member] () Shows all lobbies at this singular moment")
    async def lobby(self, ctx):
        with open("server_settings.json", "r") as ss:
            server_setting = json.load(ss)
        with open("data.json", 'r') as dataFile:
            data = json.load(dataFile)
            text, view = await msf.lobby_report(data["lobbies"],server_setting[str(ctx.guild.id)])
            await ctx.send(text,view=view)


    @commands.has_permissions(administrator=True)
    @commands.command(help = "[Admin] () purge a channel's messages, start monitoring LWG lobbies")
    async def lobby_start(self, ctx):
    
        #Initial channel clear and message
        def check(msg):
            return True  # All messages
        await ctx.channel.purge(limit=None, check=check, bulk=True)
        await ctx.send("Very well, i'l start in 5 seconds.")
        sleep(5)


        role_ranked = discord.utils.get(ctx.guild.roles, name="ranked")

        with open("server_settings.json", "r") as settingfile:
            setting = json.load(settingfile)
            guild_setting = setting[str(ctx.guild.id)]

        global stop_monitor
        role_ranked = discord.utils.get(ctx.guild.roles, name="ranked")
        last_ranked_search_status = False
        
        notif_list_setting = []
        notif_list = []
        for i in guild_setting["notifications"]["custom"]:
            notif_list.append(False)
            notif_list_setting.append(False)

        
        while True:
            with open('../data.json', 'r') as dataFile:
                data = json.load(dataFile)
                messages = [msg async for msg in ctx.channel.history(limit=50)]
                
                
                if stop_monitor:
                    await ctx.send("Monitoring Stopped!", view=None)
                    stop_monitor = False
                    return

                # Makes sure that only 2 messages are in the channel: role giver and lobby_monitor
                for i in range(len(messages)):
                    if messages[i].author != self.bot.user:
                        await messages[i].delete()
                    elif messages[i].author == self.bot.user and i != 0:
                        await messages[i].delete()
                        
                if messages[-1].author != self.bot.user:
                    await messages[-1].delete()
                else:
                    text, view = await msf.monitor_report(data, role_ranked, guild_setting)
                    await messages[-1].edit(content=text ,view=view)
                
                
            #Notifications
                #Ranked Notification
                if guild_setting["notifications"]["ranked"] == True:
                    if data["searching"] == True and last_ranked_search_status == False:
                        last_ranked_search_status = True
                        self.bot.ranked_notice_message = await ctx.send(f"{role_ranked.mention}")
                        await self.bot.ranked_notice_message.delete()
                    elif data["searching"] == False:
                        last_ranked_search_status = False
                        
                #Custom_role Notifications
                count = 0
                for i in guild_setting["notifications"]["custom"]:
                    gs = guild_setting["notifications"]["custom"]
                    map_exist = False
                    for k in data["lobbies"]:
                        if gs[i]["enabled"] == True and i.lower() in k["map"].lower():
                            map_exist = True
                    
                    if map_exist:
                        notif_list[count] = True
                    else:
                        notif_list[count] = False
                    count += 1
                

                notif_list_count = 0
                for i in guild_setting["notifications"]["custom"]:
                    if notif_list[notif_list_count] == True and notif_list_setting[notif_list_count] == False:
                        notif_list_setting[notif_list_count] = True
                        self.bot.ranked_notice_message = await ctx.send(f"{discord.utils.get(ctx.guild.roles, name = i).mention}")
                        await self.bot.ranked_notice_message.delete()
                    elif notif_list[notif_list_count] == False:
                        notif_list_setting[notif_list_count] = False
                    notif_list_count += 1
                notif_list_count = 0
                


            sleep(2)
        
    @commands.has_permissions(administrator=True)
    @commands.command(help="[Admin] () stops !lobby_start command")
    async def lobby_stop(self, ctx):
        global stop_monitor
        stop_monitor =  True

    

async def setup(bot):
    await bot.add_cog(Lobby(bot))
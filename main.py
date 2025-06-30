import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from time import sleep
import json
import sys
import subprocess

import msg_funcs as msf

from keep_alive import keep_alive


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

keep_alive()

handler = logging.FileHandler(filename='discord.log', encoding='utf8', mode='w')
intents = discord.Intents.default()
intents.message_content = True


stop_monitor = False
rank_notice = True

# ---- use only ONE bot instance ----
# class MyBot(commands.Bot):
#     async def setup_hook(self):
#         await self.load_extension("cogs.test")
#         await self.load_extension("cogs.cog_lobby")

# bot = MyBot(command_prefix="!", intents=intents)   # ← reused everywhere below
# -----------------------------------

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready to rumble!')

@bot.event
async def on_guild_join(ctx, guild):
    with open("server_settings.json", "r") as ss:
        server_settings = json.load(ss)
    
    if guild.id not in server_settings: 
        server_settings[ctx.guild.id]  = {
            "notifications":{
                    "ranked" : False,
                    "custom" : {}
                }
            }
        with open("server_settings.json", "w") as ss:
            json.dump(server_settings, ss, indent=4)




@commands.has_permissions(administrator=True)
@bot.command(help="[Admin] () if server has no settings file, adds it for that server")
async def add_server_setting(ctx):
    with open("server_settings.json", "r") as ss:
        server_settings = json.load(ss)
    
    if ctx.guild.id not in server_settings: 
        server_settings[ctx.guild.id]  = {
            "notifications":{
                    "ranked" : False,
                    "custom" : {}
                }
            }
        with open("server_settings.json", "w") as ss:
            json.dump(server_settings, ss, indent=4)

# ---------------------------------------------------------------------------- #
#                             Scraper Bot Handling                             #
# ---------------------------------------------------------------------------- #

reporter_process = None

@commands.has_permissions(administrator=True)
@bot.command(help = "[Admin] () Start the scraper")
async def reporter_start(ctx):
    global reporter_process
    if reporter_process is None:
        reporter_process = subprocess.Popen(['python', 'reporter.py'])
        await ctx.send("Reporter reporting for duty!.")
    else:
        await ctx.send("Reporter already reporting!.")


@commands.has_permissions(administrator=True)
@bot.command(help = "[Admin] () Stop the scraper")
async def reporter_stop(ctx):
    global reporter_process
    if reporter_process:
        reporter_process.terminate()
        reporter_process = None
        await ctx.send("Reporter dismissed.")
    else:
        await ctx.send("Reporter is already offduty.")




# ---------------------------------------------------------------------------- #
#                         Lobby and Monitoring Cmmands                         #
# ---------------------------------------------------------------------------- #

@bot.command(help = "[Member] () Shows all lobbies at this singular moment")
async def lobby(ctx):
    with open("server_settings.json", "r") as ss:
        server_setting = json.load(ss)
    with open("data.json", 'r') as dataFile:
        data = json.load(dataFile)
        text, view = await msf.lobby_report(data["lobbies"],server_setting[str(ctx.guild.id)])
        await ctx.send(text,view=view)


@commands.has_permissions(administrator=True)
@bot.command(help = "[Admin] () purge a channel's messages, start monitoring LWG lobbies")
async def lobby_start(ctx):
 
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
        with open('data.json', 'r') as dataFile:
            data = json.load(dataFile)
            messages = [msg async for msg in ctx.channel.history(limit=50)]
            
            
            if stop_monitor:
                await ctx.send("Monitoring Stopped!", view=None)
                stop_monitor = False
                return

            # Makes sure that only 2 messages are in the channel: role giver and lobby_monitor
            for i in range(len(messages)):
                if messages[i].author != bot.user:
                    await messages[i].delete()
                elif messages[i].author == bot.user and i != 0:
                    await messages[i].delete()
                    
            if messages[-1].author != bot.user:
                await messages[-1].delete()
            else:
                text, view = await msf.monitor_report(data, role_ranked, guild_setting)
                await messages[-1].edit(content=text ,view=view)
            
            
        #Notifications
            #Ranked Notification
            if guild_setting["notifications"]["ranked"] == True:
                if data["searching"] == True and last_ranked_search_status == False:
                    last_ranked_search_status = True
                    bot.ranked_notice_message = await ctx.send(f"{role_ranked.mention}")
                    await bot.ranked_notice_message.delete()
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
                    bot.ranked_notice_message = await ctx.send(f"{discord.utils.get(ctx.guild.roles, name = i).mention}")
                    await bot.ranked_notice_message.delete()
                elif notif_list[notif_list_count] == False:
                    notif_list_setting[notif_list_count] = False
                notif_list_count += 1
            notif_list_count = 0
            


        sleep(2)
    
@commands.has_permissions(administrator=True)
@bot.command(help="[Admin] () stops !lobby_start command")
async def lobby_stop(ctx):
    global stop_monitor
    stop_monitor =  True

# ---------------------------------------------------------------------------- #
#                                 Bot Commands                                 #
# ---------------------------------------------------------------------------- #

@bot.command(help = "[Member] () Says hi :D")
async def hi(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@commands.has_permissions(manage_messages=True)
@bot.command(help = "[Admin] () clears all messages sent in the past 14 days")
async def bot_clear_all(ctx):
    def check(msg):
        return True  # All messages
    await ctx.channel.purge(limit=None, check=check, bulk=True)

@commands.has_permissions(administrator=True)
@bot.command(help = "[Admin] () shuts the bot down")
async def bot_shutdown(ctx):
    global reporter_process
    lobby_stop(ctx)
    if reporter_process:
        reporter_process.terminate()
        reporter_process = None
    await ctx.send("Shutting down...")
    await bot.close()
    sys.exit()  # Optional: exits Python process
    
@commands.has_permissions(administrator=True)
@bot.command(help = "[Admin] () Restarts the bot")
async def bot_restart(ctx):
    lobby_stop(ctx)
    await ctx.send("Restarting...")
    await bot.close()
    os.execv(sys.executable, ['python'] + sys.argv)

# ---------------------------------------------------------------------------- #
#                                 Role Commands                                #
# ---------------------------------------------------------------------------- #

@bot.command(help = "[Member] (role_name) Give yourself a map role if it exist")
async def role_get(ctx, role_name):
    with open("server_settings.json", "r") as ss:
        ss = json.load(ss)
        server_settings = ss[str(ctx.guild.id)]["notifications"]["custom"]

        role = discord.utils.get(ctx.guild.roles, name = role_name)

        if role_name.lower() != "ranked" and role_name.lower() not in server_settings.keys():
            await ctx.send("i cant find this role. CHECK YOUR SPELLING SWINE!")
        elif role in ctx.author.roles:
            await ctx.send(f"{ctx.author.mention}, you already have this role!")
        else:
            await ctx.author.add_roles(role)
            await ctx.send(f"Congrats {ctx.author.mention}! you now have {role} role!")



@bot.command(help = "[Member] (role_name) remove a role you have")
async def role_remove(ctx, role_name):
    with open("server_settings.json", "r") as ss:
        ss = json.load(ss)
        server_settings = ss[str(ctx.guild.id)]["notifications"]["custom"]

        role = discord.utils.get(ctx.guild.roles, name = role_name)

        if role_name.lower() != "ranked" and role_name.lower() not in server_settings.keys():
            await ctx.send("i cant find this role. CHECK YOUR SPELLING SWINE!")
        elif role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.send(f"Very well {ctx.author.mention}! your {role} role has been removed!")
        else:
            await ctx.send(f"Sry {ctx.author.mention}, You dont have this role :(")



# ---------------------------------------------------------------------------- #
#                         Notification Toggle Commands                         #
# ---------------------------------------------------------------------------- #

@commands.has_permissions(administrator=True)
@bot.command(help = "[Admin] () Enable/Disable rank notification")
async def notif_ranked(ctx):
    with open("server_settings.json","r") as ss:
        server_setting = json.load(ss)
        rank_notice = server_setting[str(ctx.guild.id)]["notifications"]

    if rank_notice == True:
        rank_notice["ranked"] = False
        await ctx.send("Ranked notification: Disabled")
    else:
        rank_notice["ranked"] = True
        await ctx.send("Ranked notification: Enabled")

    with open("server_settings.json","w") as ss:
        json.dump(server_setting, ss, indent=4)

@commands.has_permissions(administrator=True)
@bot.command(help = "[Admin] (role_name) Enable/Disable rank notification")
async def notif_custom(ctx, role):
    with open("server_settings.json","r") as ss:
        server_setting = json.load(ss)
    role_notif = server_setting[str(ctx.guild.id)]["notifications"]["custom"][role]["enabled"]

    if role not in server_setting[str(ctx.guild.id)]["notifications"]["custom"]:
        await ctx.send("This role doesnt exist in filter list")
        return
    
    if role_notif == True:
        server_setting[str(ctx.guild.id)]["notifications"]["custom"][role]["enabled"] = False
        await ctx.send(f"{role}'s notification is now disabled")
    else:
        server_setting[str(ctx.guild.id)]["notifications"]["custom"][role]["enabled"] = True
        await ctx.send(f"{role}'s notification is now enabled")

    with open("server_settings.json","w") as ss:
        json.dump(server_setting, ss, indent=4)
# ---------------------------------------------------------------------------- #
#                                Filter Commands                               #
# ---------------------------------------------------------------------------- #

@bot.command(help = "[Member] () displays a list of filters.")
async def filter_view(ctx):
    with open("server_settings.json", "r") as ss:
        server_settings = json.load(ss)
        server_roles = server_settings[str(ctx.guild.id)]["notifications"]["custom"]
        await ctx.send("".join(list(f"> {i}: {server_roles[i]} \n" for i in server_roles)))

@commands.has_permissions(administrator=True)
@bot.command(help = "[Admin] (role_name, map_name) add a new filter.")
async def filter_add(ctx, role, map_name):
    with open("server_settings.json","r") as ss:
        server_set = json.load(ss)
    setting_custom = server_set[str(ctx.guild.id)]["notifications"]["custom"]
    setting_custom[role] = dict(map = map_name ,enabled=False)
    with open("server_settings.json","w") as ss2:
        json.dump(server_set, ss2, indent=4)
    guild = ctx.guild
    await guild.create_role(name=role)
    await ctx.send(f"{role} filter is added. \n Current filters:")
    await filter_view(ctx)


# @commands.has_permissions(administrator=True)
# @bot.command(help = "[Admin] (old_role, new_role, new_map) edit a filters.")
# async def filter_edit(ctx, old_role, new_role, new_map):
#     with open("server_settings.json", "r") as ss:
#         server_settings = json.load(ss)
#         server_settings[str(ctx.guild.id)]["notifications"]["custom"].pop(old_role)
#         setting_custom[new_role] = dict(map = new_map ,enabled=False)
#     with open("server_settings.json","w") as ss2:
#         json.dump(server_set, ss2, indent=4)
#     await ctx.send(f"It is done")
#     await filter_view(ctx)


@commands.has_permissions(administrator=True)
@bot.command(help = "[Admin] (role_name) removes a filter.")
async def filter_remove(ctx, role):
    with open("server_settings.json", "r") as ss:
        server_settings = json.load(ss)
        server_settings[str(ctx.guild.id)]["notifications"]["custom"].pop(role)
    
    with open("server_settings.json", "w") as ss:
        json.dump(server_settings,ss, indent=4)
    try:
        await role.delete()
        await ctx.send(f"Role `{role.name}` has been deleted.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete that role.")
    except discord.HTTPException as e:
        await ctx.send(f"Failed to delete role: {e}")

    await ctx.send(f"{role} filter is removed. \n Current filters:")
    await filter_view(ctx)
    

def main():
    bot.run(token, log_handler=handler, log_level=logging.DEBUG)

main()

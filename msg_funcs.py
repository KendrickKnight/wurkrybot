import discord 
from discord.ext import commands

lwg_link = "https://littlewargame.com/play/"
emoji_running = ":man_running_facing_right:"
emoji_lock = ":lock:"
emoji_roles = [':one:',
               ':two:',
               ':three:',
               ':four:',
               ':five:',
               ':six:',
               ':seven:',
               ':eight:',
               ':nine:',]

def link_button_view():
    view = discord.ui.View()
    item = discord.ui.Button(style=discord.ButtonStyle.link, label='Join', url=lwg_link)
    view.add_item(item=item)
 
def role_report(setting):
    roles_text = ":zero: Ranked"
    roles_dictionary = {}
    for i in range(len(setting["notifications"]["custom"])):
        roles_text += (f"\n{emoji_roles[i]}  {list(setting['notifications']['custom'].keys())[i]}")
        roles_dictionary[str(emoji_roles[i])] = str(list(setting["notifications"]["custom"].keys())[i])
    
    role_embed = discord.Embed(
        title="Roles",
        description="select the roles you wanna be notified for",
        color=discord.Color.orange()
    )
    role_embed.add_field(name=" ",value=roles_text)
    
    return role_embed, roles_dictionary

async def lobby_report(data, setting):
        # Generating message text
    lobby_text = "\n **Lobbies:** \n"
    customs_text = ""

    if len(setting["notifications"]["custom"]) > 0:
            customs_text += "\n **Filtered Lobbies:**\n"

    for i in data:
        if len(setting["notifications"]["custom"]) > 0:
            for k in setting["notifications"]["custom"]:
                if k.lower() in i["map"].lower():
                    customs_text += f"> {i["name"]} {i["player_count"]}{emoji_running if i["running"]==True else ""}{emoji_lock if i["locked"]==True else "" + "\n"}"
                else:
                    lobby_text += f"> {i["name"]} {i["player_count"]}{emoji_running if i["running"]==True else ""}{emoji_lock if i["locked"]==True else "" + "\n"}"

                
        else: lobby_text += f"\n > {i["name"]} {i["player_count"]}{emoji_running if i["running"]==True else ""}{emoji_lock if i["locked"]==True else ""}"
                
    
    text = lobby_text + customs_text

    return text, link_button_view()
        

async def monitor_report(data, ranked, setting):

    connection_text = "**Reporter Status:**"
    ranked_text = "**Ranked** \n"
    lobby_text = "\n **Lobbies:** \n"
    customs_text = ""

    if data["connection"]:
        connection_text += " :green_circle: \n"
    else:
        connection_text += " :red_circle: \n"

    if data["searching"] == True:
        ranked_text += f"{ranked.mention} `Someone's Searching!` \n"
    else: 
        ranked_text += f"`No one is searching. START YOUR CRUSADE!` \n"
        last_ranked_search_status = False

    if len(setting["notifications"]["custom"]) > 0:
            customs_text += f"\n **Filtered Lobbies:**\n"

    for i in data["lobbies"]:
        if len(setting["notifications"]["custom"]) > 0:
            for k in setting["notifications"]["custom"]:
                if k.lower() in i["map"].lower():
                    customs_text += f"> {i["name"]} {i["player_count"]}{emoji_running if i["running"]==True else ""}{emoji_lock if i["locked"]==True else "" + "\n"}"
                else:
                    lobby_text += f"> {i["name"]} {i["player_count"]}{emoji_running if i["running"]==True else ""}{emoji_lock if i["locked"]==True else "" + "\n"}"

                
        else: lobby_text += f"\n > {i["name"]} {i["player_count"]}{emoji_running if i["running"]==True else ""}{emoji_lock if i["locked"]==True else ""}"
                
    
    text = connection_text + ranked_text + lobby_text + customs_text

    return text, link_button_view()

async def customs_notif(ctx, data):
    for i in data:
        role = await discord.utils.get(ctx.guild.roles, name=i)
        enabled = data[i]["notify"]
        map_name = data[i]["map"]

        if enabled:
            bot.ranked_notice_message = await ctx.send(f"{role.mention}")
            await bot.ranked_notice_message.delete()


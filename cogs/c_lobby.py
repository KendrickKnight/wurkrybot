from discord.ext import commands
import discord
import math

class Lobby(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    def role_notify(self,ctx,role): # this will be used to notify users when a lobby is created for a role
        pass

    def msg_embed_role(self,ctx,role): # embed message for giving roles
        pass

    def sort_lobbies(self,ctx): # sorts lobbies based on roles
        roles = list(self.bot.data_settings[str(ctx.guild.id)]["roles"].keys())
        lobbies = self.bot.data_lobbies["lobbies"]
        filtered_dict = {}
        
        if self.bot.data_lobbies["ranked"]:
            filtered_dict["Ranked"] = True
        else:
            filtered_dict["Ranked"] = False
            
        for role in roles:
            filtered_dict[role] = []
        filtered_dict["lobbies"] = []
        
        
        for lobby in lobbies:
            matched = False
            for role in roles:
                if role.lower() in lobby["map"].lower():
                    matched = True
                    filtered_dict[role].append(lobby)

            if not matched:
                    filtered_dict["lobbies"].append(lobby)
        return filtered_dict
        
    def msg_embed_lobby(self,ctx,role_name,lobbies): # embed message for each specified role
        lobby_msg = ""
        msg_ranked = ["someone is searching for ranked!", "no one is ranking ):"]

        if role_name == "Ranked":
            lobby_msg += msg_ranked[0] if lobbies else msg_ranked[1]
        else:
            for lobby in lobbies:
                if lobby["invite"] is not None and not lobby["locked"] and not lobby["running"]:
                    lobby_msg += f"[{lobby['name'] + " " +lobby["player_count"]}]({lobby["invite"]}){" 🔒" if lobby["locked"] else ""}{" 🏃‍♂️" if lobby["running"] else ""} \n"
                else:
                    lobby_msg += f"{lobby['name'] + " " +lobby["player_count"]}{" 🔒" if lobby["locked"] else ""}{" 🏃‍♂️" if lobby["running"] else ""} \n"

        if role_name.lower() == "lobbies":
            color = "fafdff"
            img = "https://placehold.co/300/2F3136/2F3136"
        elif role_name.lower() == "ranked":
            color = "d62411"
            img = "https://placehold.co/300/2F3136/2F3136"
        else:
            color = self.bot.data_settings[str(ctx.guild.id)]["roles"][role_name]["color"]
            img = self.bot.data_settings[str(ctx.guild.id)]["roles"][role_name]["img"]


        # Making sure all embed boxes have the same length, character_wise
        # dl = 50 # Desired Length
        # rl = math.ceil((dl - len(role_name))/2) #remaining length
        
        # if len(role_name) < dl:
        #     if rl % 2 == 0:
        #         role_name += "\u2007\u200b"*rl
        #     else:
        #         role_name += (" \u2007"+"\u200b\u2007"*rl)

        spacer = "\u2007\u200b" * 35

        # Embed message itself
        embed = discord.Embed(
            title=f"{role_name}",
            description=f"{lobby_msg} ",
            colour=discord.Colour(int(color, 16))
        )
        embed.set_thumbnail(url=img)
        embed.set_footer(text=f"{spacer}",icon_url=ctx.bot.user.display_avatar.url)
        
        
        return embed

    @commands.command()
    async def lobby(self,ctx):
        filtered_dict = self.sort_lobbies(ctx)
        message = ""
        embeds = []  
        
        for role in filtered_dict:
            embeds.append(self.msg_embed_lobby(ctx,role,filtered_dict[role]))
        
        await ctx.send(message,embeds=embeds)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rls(self,ctx):
        roles = self.bot.data_settings[str(ctx.guild.id)]["roles"]
        
        
        embed = discord.Embed(
            title="React 4 Roles",
            description="Get notified for open lobbies by reacting the emoji of your desired role!",
            colour=discord.Colour.blue()
        )
        embed.add_field(name="Roles", value="\n".join([f"{roles[role]['emoji']} {role}" for role in roles]), inline=True)
        embed.set_thumbnail(url="https://placehold.co/300/2F3136/2F3136")
        
        await ctx.send(embed=embed)
        
    


async def setup(bot):
    await bot.add_cog(Lobby(bot))
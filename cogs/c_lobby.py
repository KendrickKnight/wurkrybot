from discord.ext import commands
import discord
import asyncio

class Lobby(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    async def role_notify(self,ctx,role_name): # this will be used to notify users when a lobby is created for a role
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            msg_notif_role = await ctx.send(f"> {role.mention} lobby created")
            await msg_notif_role.delete()

    def msg_embed_role(self,ctx): # embed message for giving roles
        roles = self.bot.data_settings[str(ctx.guild.id)]["roles"]

        embed = discord.Embed(
            title="React 4 Roles",
            description="Get notified for open lobbies by reacting the emoji of your desired role!",
            colour=discord.Colour.blue()
        )
        embed.add_field(name="Roles", value="\n".join([f"{roles[role]['emoji']} {role}" for role in roles]), inline=True)
        embed.set_thumbnail(url="https://placehold.co/300/2F3136/2F3136")

        return embed

    def sort_lobbies(self,ctx): # sorts lobbies based on roles
        roles = list(self.bot.data_settings[str(ctx.guild.id)]["roles"].keys())
        lobbies = self.bot.data_lobbies["lobbies"]
        filtered_dict = {}
        
        if self.bot.data_lobbies["ranked"]:
            filtered_dict["ranked"] = True
        else:
            filtered_dict["ranked"] = False
            
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

        if role_name == "ranked":
            lobby_msg += msg_ranked[0] if self.bot.data_lobbies["ranked"] else msg_ranked[1]
        else:
            for lobby in lobbies:
                if lobby["invite"] is not None and not lobby["locked"] and not lobby["running"]:
                    lobby_msg += f"[{lobby['name'] + " " +lobby["player_count"]}]({lobby["invite"]}){" 🔒" if lobby["locked"] else ""}{" 🏃‍♂️" if lobby["running"] else ""} \n"
                else:
                    lobby_msg += f"{lobby['name'] + " " +lobby["player_count"]}{" 🔒" if lobby["locked"] else ""}{" 🏃‍♂️" if lobby["running"] else ""} \n"

        if role_name.lower() == "lobbies":
            color = "fafdff"
            img = "https://dummyimage.com/300x300/131416/131416.png"
        elif role_name.lower() == "ranked":
            color = "d62411"
            img = "https://dummyimage.com/300x300/131416/131416.png"
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

        spacer = "\u2007\u200b" * 50

        # Embed message itself
        embed = discord.Embed(
            title=f"{role_name}",
            description=f"{lobby_msg} ",
            colour=discord.Colour(int(color, 16))
        )
        embed.set_thumbnail(url=img)
        embed.set_footer(text=f"{spacer}",icon_url=ctx.bot.user.display_avatar.url)
        
        
        return embed

    @commands.command(brief="[M] Shows all lobbies.")
    async def lobby(self,ctx):
        filtered_dict = self.sort_lobbies(ctx)
        message = ""
        embeds = []  
        
        for role in filtered_dict:
            embeds.append(self.msg_embed_lobby(ctx,role,filtered_dict[role]))
        
        await ctx.send(message,embeds=embeds)

    @commands.command(brief="[A] Displays all roles this server has on settings.json")
    @commands.has_permissions(administrator=True)
    async def rls(self,ctx):
        embed = self.msg_embed_role(ctx)
        
        await ctx.send(embed=embed)
        
    @commands.command(brief="[A] Starts the lobby report.")
    @commands.has_permissions(administrator=True)
    async def lob_start(self,ctx):

        self.bot.data_notifs[str(ctx.guild.id)]["running"] = True

        

        msg_role = await ctx.send(embed=self.msg_embed_role(ctx))
        for role in self.bot.data_settings[str(ctx.guild.id)]["roles"]:
            await msg_role.add_reaction(self.bot.data_settings[str(ctx.guild.id)]["roles"][role]["emoji"])
        self.bot.data_notifs[str(ctx.guild.id)]["msg_role"] = msg_role.id


        filtered_dict = self.sort_lobbies(ctx)
        lobby_embed = [self.msg_embed_lobby(ctx,role,filtered_dict[role]) for role in filtered_dict]  

        msg_lobby = await ctx.send(embeds=lobby_embed)

        while True:
            notify = self.bot.data_settings[str(ctx.guild.id)]["notify"]
            
            running = self.bot.data_notifs[str(ctx.guild.id)]["running"]
            if not running:
                await msg_role.delete()
                await msg_lobby.delete()
                msg_stop = await ctx.send("> Lobby report stopped")
                await asyncio.sleep(5)
                await msg_stop.delete()
                break
            
            filtered_dict = self.sort_lobbies(ctx)
            lobby_embed = [self.msg_embed_lobby(ctx,role,filtered_dict[role]) for role in filtered_dict]

            msg_role = await ctx.fetch_message(self.bot.data_notifs[str(ctx.guild.id)]["msg_role"])
            # ✅ Get the set of emojis that *should* be on the message
            allowed_emojis = {
                role_data["emoji"]
                for role_data in self.bot.data_settings[str(ctx.guild.id)]["roles"].values()
            }

            # ✅ Get current emojis on the message
            current_emojis = { str(reaction.emoji) for reaction in msg_role.reactions }
            
            # ✅ Remove reactions that are not in allowed list
            for reaction in msg_role.reactions:
                if str(reaction.emoji) not in allowed_emojis:
                    await msg_role.clear_reaction(reaction.emoji)

            # ✅ Add reactions for any new roles missing from the message
            for emoji in allowed_emojis:
                if emoji not in current_emojis:
                    await msg_role.add_reaction(emoji)

            await msg_lobby.edit(embeds=lobby_embed)
            await msg_role.edit(embed=self.msg_embed_role(ctx))
            await asyncio.sleep(5)
            
            notif = ""
            if notify:
                for role in filtered_dict:
                    if role == "lobbies":
                        continue
                        
                    if role == "ranked":
                        if self.bot.data_lobbies["ranked"] and not self.bot.data_notifs[str(ctx.guild.id)][role]:
                            notif +=  f"{discord.utils.get(ctx.guild.roles, name="ranked").mention}"
                            self.bot.data_notifs[str(ctx.guild.id)][role] = True
                        elif not self.bot.data_lobbies["ranked"]:
                            self.bot.data_notifs[str(ctx.guild.id)][role] = False
                        continue
                    
                    if filtered_dict[role] != [] and not self.bot.data_notifs[str(ctx.guild.id)][role]:
                        try:
                            notif +=  f"{discord.utils.get(ctx.guild.roles, name=role).mention}"
                            self.bot.data_notifs[str(ctx.guild.id)][role] = True
                        except AttributeError:
                            msg_att_err = await ctx.send(f"> Role {role} does not exist in this server")
                            await asyncio.sleep(5)
                            await msg_att_err.delete()
                        except Exception as e:
                            print(e)
                    elif filtered_dict[role] == []:
                        self.bot.data_notifs[str(ctx.guild.id)][role] = False

                if notif != "":
                    msg_notif = await ctx.send(notif)
                    await msg_notif.delete()
                    notif = ""
            
        

    @commands.command(brief="[A] Stops the lobby report.")
    @commands.has_permissions(administrator=True)
    async def lob_stop(self,ctx):
        if "running" in self.bot.data_notifs[str(ctx.guild.id)]:
            self.bot.data_notifs[str(ctx.guild.id)]["running"] = False
        else: 
            await ctx.send("> Lobby report is not running")
    

async def setup(bot):
    await bot.add_cog(Lobby(bot))
from discord.ext import commands
import asyncio 
import util
import random

class Test(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command(brief="[M] Generate random lobbies!", help="!gen_lobby <map_name> <map_name> <map_name> ... \n basically you can add map name and it will generate lobbies for that map. if you dont add any map name it will generate lobbies for all maps.\n this function will either be removed or hidden on the final version.")
    async def gen_lobby(self,ctx,*args):
        generated_lobbies = []
        
        host_name = "lobbyGent"
        invite_code = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        map_quantity_chances = [0,0,0,0,1,1,1,2,2,3] # basically deciding how many of each lobby to generate
        maps = { # "Map name" : Max players
            "Raid Wars Classic":{"max_players":2 ,"isArgument" : False},
            "Anarking":{"max_players":6 ,"isArgument" : False},
            "Ravaged":{"max_players":2 ,"isArgument" : False},
            "TowerDefense Kingdome":{"max_players":6 ,"isArgument" : False},
            "Rothaga":{"max_players":4 ,"isArgument" : False},
            "Woof":{"max_players":6 ,"isArgument" : False}
        }

        for map in args:
            if map in maps:
                maps[map]["isArgument"] = True
            else:
                maps[map] = {"max_players": random.randint(2,6) ,"isArgument" : True}
        
        
        def gen_lobby_att(map): # this fellas takes a dictionary of a map and returns a dictionary of the lobby attributes for the json file
            
            name = map
            host = f"{host_name}_{random.randint(100000,999999)}"
            map = map
            player_count = f"[{random.randint(1,maps[map]["max_players"])}/{maps[map]["max_players"]}]"
            locked = True if random.randint(0,10) == 10 else False
            running = True if random.randint(0,5) == 5 else False
            invite = f"<{invite_code}>" if not locked else None
                
            lobby = {"name":name,"host":host,"map":map,"player_count":player_count,"locked":locked,"running":running,"invite":invite}
            return lobby
    
        

        for map in maps:
            if maps[map]["isArgument"]:
                for i in range(random.randint(1,3)):
                    generated_lobbies.append(gen_lobby_att(map))
            else:
                for i in range(random.choice(map_quantity_chances)):
                    generated_lobbies.append(gen_lobby_att(map))
            
        self.bot.data_lobbies["lobbies"] = generated_lobbies
        util.syncData("lobbies",cmd=False,inputData=self.bot.data_lobbies)
        
        msg_gen_lobby = await ctx.send("> Lobbies Generated!")

        await asyncio.sleep(3)
        await msg_gen_lobby.delete()
        await ctx.message.delete()
    
    @commands.command(brief="[M] Toggle ranked lobby! like weither someone is searching or not")
    async def gen_ranked(self,ctx):
        if self.bot.data_lobbies["ranked"]:
            self.bot.data_lobbies["ranked"] = False
            util.syncData("lobbies",cmd=False,inputData=self.bot.data_lobbies)
            
            msg_ranked = await ctx.send("> no one is seaching for ranked now")
            await asyncio.sleep(5)
            await msg_ranked.delete()
            await ctx.message.delete()

        else: 
            self.bot.data_lobbies["ranked"] = True
            util.syncData("lobbies",cmd=False,inputData=self.bot.data_lobbies)
            
            msg_ranked = await ctx.send("> someone is searching for ranked now")
            await asyncio.sleep(5)
            await msg_ranked.delete()
            await ctx.message.delete()

    @commands.command(brief="[D] Debugs the role (owner only).",hidden=True)
    @commands.is_owner()
    async def debugroles(self, ctx):
        print(self.bot.data_settings[str(ctx.guild.id)]["roles"].keys())
            
async def setup(bot):
    await bot.add_cog(Test(bot))
from discord.ext import commands

Class Events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    # @commands.Cog.listener()
    # async def on_ready(self):
    #   guild_id = str(ctx.guild.id)
    #   roles = self.bot.data_settings[str(ctx.guild.id)]["roles"]
    #   pass

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
      if self.bot.data_settings[str(guild.id)]:
          pass
      else:
          self.bot.data_settings[str(guild.id)] = {
              "notify":True,
              "roles":{
                  "ranked" : False,
              }
          }




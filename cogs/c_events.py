from discord.ext import commands
import discord
import util

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}, ready to rumble >:D")

        # Ensure notification structure exists
        self.bot.data_notifs = {}
        for guild in self.bot.data_settings:
            self.bot.data_notifs[str(guild)] = {}  # init first
            for role in self.bot.data_settings[guild]["roles"]:
                self.bot.data_notifs[str(guild)][role] = False

        # if self.bot.data_notifs != {}:
        #     print(self.bot.data_notifs)
        #     print("data_notifs is populated!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # Ensure guild settings exist
        if str(guild.id) not in self.bot.data_settings:
            self.bot.data_settings[str(guild.id)] = {
                "notifs": True,
                "roles": {
                    "ranked": False,
                }
            }
            util.syncData("settings", cmd=False, inputData=self.bot.data_settings)

        # Ensure notify structure exists
        if str(guild.id) not in self.bot.data_notifs:
            self.bot.data_notifs[str(guild.id)] = {}
            for role in self.bot.data_settings[str(guild.id)]["roles"]:
                self.bot.data_notifs[str(guild.id)][role] = False

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        if str(guild.id) in self.bot.data_settings:
            del self.bot.data_settings[str(guild.id)]
            util.syncData("settings", cmd=False, inputData=self.bot.data_settings)

        if str(guild.id) in self.bot.data_notifs:
            del self.bot.data_notifs[str(guild.id)]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        # ensure we have a member
        member = payload.member
        if member is None:
            member = await guild.fetch_member(payload.user_id)

        # ignore bots
        if member.bot:
            return

        guild_id = str(payload.guild_id)
        emoji = str(payload.emoji)

        for role_name, role_data in self.bot.data_settings[guild_id]["roles"].items():
            # match by emoji carefully
            if role_data["emoji"] == emoji:
                # better to store role ID in your settings
                guild_role = discord.utils.get(guild.roles, name=role_name)
                if guild_role:
                    await member.add_roles(guild_role)
                    break
    
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        guild_id = str(payload.guild_id)
        emoji = str(payload.emoji)
    
        for role, role_data in self.bot.data_settings[guild_id]["roles"].items():
            if role_data["emoji"] == emoji:
                guild = self.bot.get_guild(payload.guild_id)
                guild_role = discord.utils.get(guild.roles, name=role)
                member = guild.get_member(payload.user_id)
                if guild_role and member and not member.bot:
                    await member.remove_roles(guild_role)
                    break


async def setup(bot):
    await bot.add_cog(Events(bot))
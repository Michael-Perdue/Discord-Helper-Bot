import discord
from discord.ext import commands

class Messaging(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(name="spam")
    async def spam(self,ctx):
        await ctx.send("test")

async def setup(bot):
    await bot.add_cog(Messaging(bot))
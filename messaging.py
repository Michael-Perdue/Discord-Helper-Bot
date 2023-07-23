import discord
from discord.ext import commands
from time import sleep
class Messaging(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self,ctx):
        await ctx.send("Test")

    @commands.command(name="mirror")
    async def mirror(self,ctx,arg):
        await ctx.send(str(arg))

async def setup(bot):
    await bot.add_cog(Messaging(bot))